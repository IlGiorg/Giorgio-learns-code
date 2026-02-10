import React, { useEffect, useState, useRef } from "react";
import { motion } from "framer-motion";

// Rail Signalling Simulator - Single-file React component with:
// - animated train movement (framer-motion)
// - AI scheduling (auto-assign simple heuristic)
// - conflict detection (prevent double-assignment of same platform)
// - CSV import/export of trains
// - PDF export of departure board (uses dynamic import of jspdf if installed)
// Audio announcements will be added later as requested.

export default function App() {
  // --- Data model ---
  const initialStations = [
    { id: "central", name: "Central (10 platforms)", platforms: 10 },
    { id: "westj", name: "West Junction (4)", platforms: 4 },
    { id: "mid", name: "Midline (7)", platforms: 7 },
    { id: "northend", name: "North End (4)", platforms: 4 },
    { id: "southend", name: "South End (4)", platforms: 4 },
  ];

  const initialRoutes = [
    { id: "r1", name: "Central → West → Mid → North End", path: ["central", "westj", "mid", "northend"] },
    { id: "r2", name: "Central → West → Mid → South End", path: ["central", "westj", "mid", "southend"] },
    { id: "r3", name: "North End → Mid → West → Central", path: ["northend", "mid", "westj", "central"] },
    { id: "r4", name: "South End → Mid → West → Central", path: ["southend", "mid", "westj", "central"] },
  ];

  const initialTrains = [
    { id: "T1", name: "1001", status: "scheduled", routeId: null, platform: null, dep: "09:00", progress: 0 },
    { id: "T2", name: "1002", status: "scheduled", routeId: null, platform: null, dep: "09:10", progress: 0 },
    { id: "T3", name: "1003", status: "scheduled", routeId: null, platform: null, dep: "09:15", progress: 0 },
    { id: "T4", name: "1004", status: "scheduled", routeId: null, platform: null, dep: "09:20", progress: 0 },
    { id: "T5", name: "1005", status: "scheduled", routeId: null, platform: null, dep: "09:30", progress: 0 },
  ];

  // station positions (px) for the visual map (SVG)
  const stationPos = {
    central: { x: 80, y: 150 },
    westj: { x: 260, y: 150 },
    mid: { x: 460, y: 150 },
    northend: { x: 760, y: 80 },
    southend: { x: 760, y: 220 },
  };

  // --- State ---
  const [stations] = useState(initialStations);
  const [routes] = useState(initialRoutes);
  const [trains, setTrains] = useState(() => {
    try {
      const p = localStorage.getItem("rsim_trains");
      return p ? JSON.parse(p) : initialTrains;
    } catch (e) {
      return initialTrains;
    }
  });

  // Signals keyed by from_to (e.g. central_westj). default green.
  const makeDefaultSignals = () => {
    const s = {};
    const pairs = [
      ["central", "westj"],
      ["westj", "mid"],
      ["mid", "northend"],
      ["mid", "southend"],
      ["northend", "mid"],
      ["southend", "mid"],
      ["mid", "westj"],
      ["westj", "central"],
    ];
    pairs.forEach(([a, b]) => (s[`${a}_${b}`] = "green"));
    return s;
  };

  const [signals, setSignals] = useState(() => {
    try {
      const p = localStorage.getItem("rsim_signals");
      return p ? JSON.parse(p) : makeDefaultSignals();
    } catch (e) {
      return makeDefaultSignals();
    }
  });

  const [view, setView] = useState("departure");
  const [selectedTrain, setSelectedTrain] = useState(null);
  const [filter, setFilter] = useState("");

  // Simulation controls
  const [running, setRunning] = useState(false);
  const [speed, setSpeed] = useState(1); // multiplier for simulation speed

  // Save to localStorage
  useEffect(() => {
    localStorage.setItem("rsim_trains", JSON.stringify(trains));
  }, [trains]);
  useEffect(() => {
    localStorage.setItem("rsim_signals", JSON.stringify(signals));
  }, [signals]);

  // --- Helpers ---
  const stationsById = Object.fromEntries(stations.map((s) => [s.id, s]));

  function statusBadge(t) {
    if (t.status === "assigned") return <span className="px-2 py-1 rounded bg-emerald-200">Assigned</span>;
    if (t.status === "scheduled") return <span className="px-2 py-1 rounded bg-slate-200">Scheduled</span>;
    if (t.status === "moving") return <span className="px-2 py-1 rounded bg-emerald-300">Moving</span>;
    if (t.status === "late") return <span className="px-2 py-1 rounded bg-amber-300">Late +{t.lateBy}m</span>;
    if (t.status === "cancelled") return <span className="px-2 py-1 rounded bg-red-400 text-white">Cancelled</span>;
    if (t.status === "arrived") return <span className="px-2 py-1 rounded bg-sky-200">Arrived</span>;
    return <span className="px-2 py-1 rounded bg-gray-200">{t.status}</span>;
  }

  function toggleSignal(key) {
    setSignals((s) => ({ ...s, [key]: s[key] === "green" ? "red" : "green" }));
  }

  // Build route geometric info (lengths, cumulative)
  const routeGeometry = {};
  routes.forEach((r) => {
    const coords = r.path.map((id) => stationPos[id]);
    const segLengths = [];
    let total = 0;
    for (let i = 0; i < coords.length - 1; i++) {
      const dx = coords[i + 1].x - coords[i].x;
      const dy = coords[i + 1].y - coords[i].y;
      const l = Math.sqrt(dx * dx + dy * dy);
      segLengths.push(l);
      total += l;
    }
    const cumul = [0];
    let s = 0;
    segLengths.forEach((l) => {
      s += l;
      cumul.push(s);
    });
    routeGeometry[r.id] = { coords, segLengths, totalLength: total, cumul };
  });

  // Given routeId and progress [0..1], return x,y point on route
  function getPointAlongRoute(routeId, progress) {
    const g = routeGeometry[routeId];
    if (!g) return { x: -20, y: -20 };
    const dist = Math.max(0, Math.min(1, progress)) * g.totalLength;
    // find segment
    let segIdx = 0;
    while (segIdx < g.segLengths.length && dist > g.cumul[segIdx + 1]) segIdx++;
    const segStart = g.coords[segIdx];
    const segEnd = g.coords[segIdx + 1] || segStart;
    const segDist = dist - g.cumul[segIdx];
    const segLen = g.segLengths[segIdx] || 1;
    const t = segLen === 0 ? 0 : segDist / segLen;
    const x = segStart.x + (segEnd.x - segStart.x) * t;
    const y = segStart.y + (segEnd.y - segStart.y) * t;
    return { x, y };
  }

  // Returns the next segment key the train would enter based on its progress
  function nextSegmentKeyForTrain(train) {
    if (!train.routeId) return null;
    const g = routeGeometry[train.routeId];
    if (!g) return null;
    const dist = Math.max(0, Math.min(1, train.progress || 0)) * g.totalLength;
    // find seg index that contains dist
    let segIdx = 0;
    while (segIdx < g.segLengths.length && dist >= g.cumul[segIdx + 1]) segIdx++;
    // next segment to enter is segIdx (moving from segIdx to segIdx+1)
    const path = routes.find((r) => r.id === train.routeId).path;
    const from = path[segIdx];
    const to = path[segIdx + 1];
    if (!from || !to) return null;
    return `${from}_${to}`;
  }

  // Conflict detection: platformKey format: stationId:platformNumber
  function platformOccupied(platformKey) {
    return trains.some((t) => t.platform === platformKey && t.status !== "cancelled" && t.status !== "arrived" && t.status !== "scheduled");
  }

  function assignTrain(trainId, routeId, platform) {
    // conflict check
    if (platform && platformOccupied(platform)) {
      alert("Conflict: platform already occupied by another active train.");
      return false;
    }
    setTrains((prev) =>
      prev.map((t) => (t.id === trainId ? { ...t, routeId, platform, status: "assigned", progress: 0 } : t))
    );
    return true;
  }

  function cancelTrain(trainId, reason = "Cancelled") {
    setTrains((prev) => prev.map((t) => (t.id === trainId ? { ...t, status: "cancelled", note: reason } : t)));
  }
  function markLate(trainId, minutes = 10) {
    setTrains((prev) => prev.map((t) => (t.id === trainId ? { ...t, status: "late", lateBy: minutes } : t)));
  }
  function clearStatus(trainId) {
    setTrains((prev) => prev.map((t) => (t.id === trainId ? { ...t, status: "scheduled", routeId: null, platform: null, note: null, lateBy: null, progress: 0 } : t)));
  }

  // AI scheduling: simple heuristic - assign trains to the first free platform at their origin station
  function aiAssignAll() {
    setTrains((prev) => {
      const copy = [...prev];
      // sort by departure time (string HH:MM)
      copy.sort((a, b) => (a.dep > b.dep ? 1 : -1));
      for (const t of copy) {
        if (t.routeId || t.status === "cancelled") continue; // skip already assigned or cancelled
        // choose a route (for the demo we pick r1/r2 by name or leave unassigned)
        const candidateRoutes = routes.filter((r) => r.path[0] === "central" || r.path[0] === t.origin);
        // better: keep current UI to pick route; for AI, pick a route that starts at central if available
        const route = routes.find((r) => r.path[0] === "central") || routes[0];
        const origin = route.path[0];
        const station = stationsById[origin];
        if (!station) continue;
        // find first free platform
        let found = false;
        for (let p = 1; p <= station.platforms; p++) {
          const key = `${origin}:${p}`;
          const occupied = copy.some((other) => other.id !== t.id && other.platform === key && other.status !== "cancelled" && other.status !== "arrived" && other.status !== "scheduled");
          if (!occupied) {
            // assign
            t.routeId = route.id;
            t.platform = key;
            t.status = "assigned";
            t.progress = 0;
            found = true;
            break;
          }
        }
        if (!found) {
          // leave unassigned
        }
      }
      return copy;
    });
  }

  // CSV export
  function exportTrainsCSV() {
      const header = ["id", "name", "dep", "status", "routeId", "platform", "note", "lateBy"].join(",");
      const rows = trains.map((t) =>
        [t.id, t.name, t.dep, t.status, t.routeId ?? "", t.platform ?? "", t.note ?? "", t.lateBy ?? ""].join(",")
      );
      const csv = [header, ...rows].join("\n");
      const blob = new Blob([csv], { type: "text/csv" });
      const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "trains.csv";
    a.click();
    URL.revokeObjectURL(url);
  }

  // CSV import
  function importTrainsCSV(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      const txt = e.target.result;
      const lines = txt.split(/
?
/).filter(Boolean);
      if (lines.length < 2) return;
      const cols = lines[0].split(",").map((c) => c.trim().replace(/^"|"$/g, ""));
      const newTrains = lines.slice(1).map((ln) => {
        // naive CSV parsing for this demo
        const parts = ln.split(",");
        const obj = {};
        cols.forEach((c, i) => (obj[c] = (parts[i] || "").replace(/^"|"$/g, "")));
        return {
          id: obj.id || `T${Math.random().toString(36).slice(2, 6)}`,
          name: obj.name || obj.id || "-",
          dep: obj.dep || "00:00",
          status: obj.status || "scheduled",
          routeId: obj.routeId || null,
          platform: obj.platform || null,
          note: obj.note || null,
          lateBy: obj.lateBy ? Number(obj.lateBy) : null,
          progress: 0,
        };
      });
      setTrains(newTrains);
    };
    reader.readAsText(file);
  }

  // PDF export (uses jspdf if installed, otherwise falls back to window.print)
  async function exportPDF() {
    try {
      const { jsPDF } = await import("jspdf");
      const doc = new jsPDF();
      doc.setFontSize(18);
      doc.text("Departure Board", 14, 20);
      doc.setFontSize(11);
      let y = 30;
      doc.text("Time  | Train | Route | Platform | Status", 14, y);
      y += 6;
      trains.forEach((t) => {
        const routeName = t.routeId ? routes.find((r) => r.id === t.routeId)?.name : "—";
        const line = `${t.dep}  ${t.name}  ${routeName}  ${t.platform ?? "—"}  ${t.status}`;
        doc.text(line.slice(0, 90), 14, y);
        y += 6;
        if (y > 280) {
          doc.addPage();
          y = 20;
        }
      });
      doc.save("departure-board.pdf");
    } catch (e) {
      // fallback: open print dialog (user can save as PDF)
      window.print();
    }
  }

  // --- Simulation tick ---
  const tickRef = useRef(null);
  useEffect(() => {
    if (!running) {
      if (tickRef.current) {
        clearInterval(tickRef.current);
        tickRef.current = null;
      }
      return;
    }
    // start simulation
    tickRef.current = setInterval(() => {
      setTrains((prev) => {
        const next = prev.map((t) => {
          if (!t.routeId) return t; // nothing to do
          if (t.status === "cancelled" || t.status === "arrived" || t.status === "scheduled") return t;
          // attempt to move if signal ahead is green
          const segKey = nextSegmentKeyForTrain(t);
          if (segKey && signals[segKey] === "red") {
            // pause movement before entering the segment
            return { ...t }; // no progress change
          }
          // advance progress according to speed
          const speedPerSecond = 0.005 * speed; // tune this for realism
          const newProgress = Math.min(1, (t.progress || 0) + speedPerSecond);
          let newStatus = t.status;
          if (t.status === "assigned") newStatus = "moving";
          if (newProgress >= 1) {
            newStatus = "arrived";
          }
          return { ...t, progress: newProgress, status: newStatus };
        });
        return next;
      });
    }, 1000);
    return () => {
      if (tickRef.current) {
        clearInterval(tickRef.current);
        tickRef.current = null;
      }
    };
  }, [running, speed, signals]);

  // When train arrives, free platform after marking arrived
  useEffect(() => {
    // if any train just arrived, optionally clear platform after a delay
    const arrived = trains.filter((t) => t.status === "arrived" && t.platform);
    if (arrived.length === 0) return;
    const timers = arrived.map((t) => {
      return setTimeout(() => {
        setTrains((prev) => prev.map((x) => (x.id === t.id ? { ...x, platform: null } : x)));
      }, 3000);
    });
    return () => timers.forEach((id) => clearTimeout(id));
  }, [trains]);

  // Map/train UI components
  function Nav() {
    return (
      <nav className="flex items-center gap-3 p-3 bg-slate-800 text-white">
        <h1 className="text-xl font-semibold">Rail Signalling Simulator</h1>
        <div className="ml-4 flex gap-2">
          <button onClick={() => setView("departure")} className={btnClass(view === "departure")}>Departure Board</button>
          <button onClick={() => setView("signaller")} className={btnClass(view === "signaller")}>Signaller</button>
          <button onClick={() => setView("assignments")} className={btnClass(view === "assignments")}>Assignments</button>
          <button onClick={() => setView("late")} className={btnClass(view === "late")}>Late & Cancels</button>
        </div>
        <div className="ml-auto text-sm opacity-80">Platforms: Central(10) → West(4) → Mid(7) → split → North(4) / South(4)</div>
      </nav>
    );
  }

  function btnClass(active) {
    return `px-3 py-1 rounded ${active ? "bg-sky-500 text-white" : "bg-white/10 text-white hover:bg-white/20"}`;
  }

  function DepartureBoard() {
    const visible = trains.filter((t) => t.name.toLowerCase().includes(filter.toLowerCase()));
    return (
      <div className="p-4">
        <div className="mb-3 flex items-center gap-3">
          <input value={filter} onChange={(e) => setFilter(e.target.value)} placeholder="Filter trains..." className="px-3 py-2 rounded border w-64" />
          <button onClick={() => setFilter("")} className="px-3 py-2 bg-slate-200 rounded">Clear</button>

          <div className="ml-auto flex gap-2">
            <button onClick={() => exportTrainsCSV()} className="px-3 py-2 bg-slate-200 rounded">Export CSV</button>
            <label className="px-3 py-2 bg-white/10 rounded cursor-pointer">
              Import CSV
              <input type="file" accept=".csv" className="hidden" onChange={(e) => e.target.files && importTrainsCSV(e.target.files[0])} />
            </label>
            <button onClick={() => exportPDF()} className="px-3 py-2 bg-amber-200 rounded">Export PDF</button>
          </div>
        </div>

        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="text-slate-600">
              <th className="p-2">Train</th>
              <th className="p-2">Departure</th>
              <th className="p-2">Route</th>
              <th className="p-2">Platform</th>
              <th className="p-2">Status</th>
              <th className="p-2">Action</th>
            </tr>
          </thead>
          <tbody>
            {visible.map((t) => (
              <tr key={t.id} className="border-t">
                <td className="p-2 font-medium">{t.name}</td>
                <td className="p-2">{t.dep}</td>
                <td className="p-2">{t.routeId ? routes.find((r) => r.id === t.routeId)?.name : "—"}</td>
                <td className="p-2">{t.platform ?? "—"}</td>
                <td className="p-2">{statusBadge(t)}</td>
                <td className="p-2">
                  <div className="flex gap-2">
                    <button onClick={() => setSelectedTrain(t)} className="px-2 py-1 bg-slate-200 rounded">Manage</button>
                    <button onClick={() => markLate(t.id, 5)} className="px-2 py-1 bg-amber-300 rounded">Late</button>
                    <button onClick={() => cancelTrain(t.id)} className="px-2 py-1 bg-red-400 text-white rounded">Cancel</button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  }

  function SignallerView() {
    const segs = Object.keys(signals);
    return (
      <div className="p-4">
        <h2 className="text-lg font-semibold mb-3">Track map & signals</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="p-3 border rounded">
            <h3 className="font-medium mb-2">Signals</h3>
            <div className="flex flex-col gap-2">
              {segs.map((k) => (
                <div key={k} className="flex items-center justify-between">
                  <div className="capitalize">{k.split("_").join(" → ")}</div>
                  <div className="flex gap-2 items-center">
                    <div className={`px-3 py-1 rounded ${signals[k] === "green" ? "bg-emerald-300" : "bg-red-400 text-white"}`}>{signals[k]}</div>
                    <button onClick={() => toggleSignal(k)} className="px-2 py-1 bg-slate-200 rounded">Toggle</button>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="p-3 border rounded">
            <h3 className="font-medium mb-2">Station occupancy</h3>
            <div className="space-y-3">
              {stations.map((s) => (
                <div key={s.id} className="border p-2 rounded">
                  <div className="flex justify-between"><div className="font-semibold">{s.name}</div><div>{s.platforms} platforms</div></div>
                  <div className="mt-2 grid grid-cols-6 gap-2">
                    {Array.from({ length: Math.max(1, s.platforms) }).map((_, idx) => {
                      const platformNum = idx + 1;
                      const key = `${s.id}:${platformNum}`;
                      const occ = trains.find((t) => t.platform === key && t.status !== "cancelled");
                      return (
                        <div key={idx} className={`p-1 text-xs text-center rounded ${occ ? "bg-red-200" : "bg-slate-100"}`}>
                          {s.platforms ? platformNum : "—"}
                          <div className="truncate text-[10px]">{occ ? occ.name : "free"}</div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="mt-4 p-3 border rounded">
          <h3 className="font-medium">Quick commands</h3>
          <div className="mt-2 flex gap-2 items-center">
            <button onClick={() => setSignals(makeDefaultSignals())} className="px-3 py-1 bg-slate-200 rounded">Reset signals</button>
            <button onClick={() => { setTrains(initialTrains); localStorage.removeItem("rsim_trains"); }} className="px-3 py-1 bg-amber-200 rounded">Reset trains</button>
            <button onClick={() => { setTrains((t) => t.map((x) => ({ ...x, status: "scheduled", routeId: null, platform: null, note: null, progress: 0 }))); }} className="px-3 py-1 bg-emerald-100 rounded">Clear assignments</button>

            <div className="ml-auto flex items-center gap-2">
              <button onClick={() => setRunning((r) => !r)} className="px-3 py-1 bg-sky-200 rounded">{running ? "Pause" : "Play"}</button>
              <label className="text-sm">Speed</label>
              <input type="range" min={0.25} max={3} step={0.25} value={speed} onChange={(e) => setSpeed(Number(e.target.value))} />
              <button onClick={() => aiAssignAll()} className="px-3 py-1 bg-indigo-200 rounded">AI Assign</button>
            </div>
          </div>
        </div>

        <div className="mt-6 p-3 border rounded">
          <h3 className="font-medium mb-2">Track map</h3>
          <div className="relative w-full h-[300px] bg-slate-50">
            <svg width="100%" height="100%" viewBox="0 0 900 300" preserveAspectRatio="xMidYMid meet">
              {/* draw main lines */}
              {/* central -> westj -> mid */}
              <line x1={stationPos.central.x} y1={stationPos.central.y} x2={stationPos.westj.x} y2={stationPos.westj.y} stroke="#222" strokeWidth={4} />
              <line x1={stationPos.westj.x} y1={stationPos.westj.y} x2={stationPos.mid.x} y2={stationPos.mid.y} stroke="#222" strokeWidth={4} />
              {/* mid -> northend */}
              <line x1={stationPos.mid.x} y1={stationPos.mid.y} x2={stationPos.northend.x} y2={stationPos.northend.y} stroke="#222" strokeWidth={4} />
              {/* mid -> southend */}
              <line x1={stationPos.mid.x} y1={stationPos.mid.y} x2={stationPos.southend.x} y2={stationPos.southend.y} stroke="#222" strokeWidth={4} />

              {/* stations */}
              {Object.entries(stationPos).map(([id, p]) => (
                <g key={id}>
                  <circle cx={p.x} cy={p.y} r={14} fill="#fff" stroke="#111" strokeWidth={2} />
                  <text x={p.x} y={p.y - 20} textAnchor="middle" fontSize={12} fill="#111">{id}</text>
                </g>
              ))}

              {/* trains as small circles - we will not animate via SVG but place divs above using absolute positioning */}
            </svg>

            {/* overlay train markers */}
            {trains.map((t) => {
              if (!t.routeId) return null;
              const pt = getPointAlongRoute(t.routeId, t.progress || 0);
              return (
                <motion.div key={t.id}
                  layout
                  initial={{ translateX: pt.x - 10, translateY: pt.y - 10 }}
                  animate={{ translateX: pt.x - 10, translateY: pt.y - 10 }}
                  transition={{ ease: "linear", duration: 0.9 }}
                  style={{ position: "absolute", left: 0, top: 0, pointerEvents: "auto" }}>
                  <div className="w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold bg-sky-400 text-white border-2 border-white shadow">{t.name}</div>
                </motion.div>
              );
            })}
          </div>
        </div>
      </div>
    );
  }

  function AssignmentsView() {
    const [pickTrain, setPickTrain] = useState(null);
    const [pickRoute, setPickRoute] = useState(null);
    const [pickStation, setPickStation] = useState(null);
    const [pickPlatform, setPickPlatform] = useState(1);

    function openAssign(t) {
      setPickTrain(t);
      setPickRoute(null);
      setPickStation(null);
      setPickPlatform(1);
    }

    function doAssign() {
      if (!pickTrain || !pickRoute || !pickStation) return alert("Pick train, route and station platform");
      const platformKey = `${pickStation}:${pickPlatform}`;
      const ok = assignTrain(pickTrain.id, pickRoute.id, platformKey);
      if (ok) setPickTrain(null);
    }

    return (
      <div className="p-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="p-3 border rounded">
            <h3 className="font-medium mb-2">Trains</h3>
            <div className="space-y-2">
              {trains.map((t) => (
                <div key={t.id} className="flex items-center justify-between border p-2 rounded">
                  <div>
                    <div className="font-semibold">{t.name} <span className="text-xs text-slate-500">({t.id})</span></div>
                    <div className="text-xs">{t.dep} — {t.routeId ? routes.find((r) => r.id === t.routeId)?.name : 'Unassigned'}</div>
                  </div>
                  <div className="flex gap-2">
                    <button onClick={() => openAssign(t)} className="px-2 py-1 bg-sky-200 rounded">Assign</button>
                    <button onClick={() => clearStatus(t.id)} className="px-2 py-1 bg-slate-200 rounded">Reset</button>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="p-3 border rounded">
            <h3 className="font-medium mb-2">Assign</h3>
            {pickTrain ? (
              <div>
                <div className="mb-2">Train: <b>{pickTrain.name} ({pickTrain.id})</b></div>
                <div className="mb-2">
                  <label className="block text-sm">Route</label>
                  <select className="w-full p-2 border rounded" onChange={(e) => setPickRoute(routes.find((r) => r.id === e.target.value))} value={pickRoute?.id ?? ""}>
                    <option value="">Choose route...</option>
                    {routes.map((r) => <option key={r.id} value={r.id}>{r.name}</option>)}
                  </select>
                </div>

                <div className="mb-2">
                  <label className="block text-sm">Platform station (origin)</label>
                  <select className="w-full p-2 border rounded" onChange={(e) => setPickStation(e.target.value)} value={pickStation ?? ""}>
                    <option value="">Choose station...</option>
                    {stations.filter((s) => s.platforms > 0).map((s) => <option key={s.id} value={s.id}>{s.name}</option>)}
                  </select>
                </div>

                <div className="mb-2">
                  <label className="block text-sm">Platform number</label>
                  <input type="number" min={1} max={pickStation ? stationsById[pickStation].platforms : 10} value={pickPlatform} onChange={(e) => setPickPlatform(Number(e.target.value))} className="w-32 p-2 border rounded" />
                </div>

                <div className="flex gap-2">
                  <button onClick={doAssign} className="px-3 py-2 bg-emerald-400 rounded">Assign</button>
                  <button onClick={() => setPickTrain(null)} className="px-3 py-2 bg-slate-200 rounded">Cancel</button>
                </div>
              </div>
            ) : (
              <div className="text-sm">Select a train on the left to begin assignment.</div>
            )}
          </div>
        </div>
      </div>
    );
  }

  function LateView() {
    const late = trains.filter((t) => t.status === "late");
    const cancelled = trains.filter((t) => t.status === "cancelled");
    return (
      <div className="p-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="p-3 border rounded">
            <h3 className="font-medium mb-2">Late trains</h3>
            {late.length === 0 ? <div className="text-sm">No late trains</div> : (
              <div className="space-y-2">
                {late.map((t) => (
                  <div key={t.id} className="flex justify-between items-center border p-2 rounded">
                    <div>
                      <div className="font-semibold">{t.name}</div>
                      <div className="text-xs">Late by: {t.lateBy} minutes</div>
                    </div>
                    <div className="flex gap-2">
                      <button onClick={() => setTrains((prev) => prev.map((x) => x.id === t.id ? { ...x, status: 'assigned' } : x))} className="px-2 py-1 bg-emerald-200 rounded">Mark as assigned</button>
                      <button onClick={() => clearStatus(t.id)} className="px-2 py-1 bg-slate-200 rounded">Reset</button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          <div className="p-3 border rounded">
            <h3 className="font-medium mb-2">Cancelled trains</h3>
            {cancelled.length === 0 ? <div className="text-sm">No cancellations</div> : (
              <div className="space-y-2">
                {cancelled.map((t) => (
                  <div key={t.id} className="flex justify-between items-center border p-2 rounded">
                    <div>
                      <div className="font-semibold">{t.name}</div>
                      <div className="text-xs">Reason: {t.note ?? '—'}</div>
                    </div>
                    <div className="flex gap-2">
                      <button onClick={() => clearStatus(t.id)} className="px-2 py-1 bg-emerald-200 rounded">Reinstate</button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    );
  }

  function TrainModal({ train, onClose }) {
    if (!train) return null;
    const pt = train.routeId ? getPointAlongRoute(train.routeId, train.progress || 0) : null;
    return (
      <div className="fixed inset-0 bg-black/40 flex items-center justify-center p-4">
        <div className="bg-white rounded w-full max-w-xl p-4">
          <div className="flex justify-between items-center mb-3">
            <div>
              <h3 className="font-semibold">Manage {train.name}</h3>
              <div className="text-sm text-slate-500">ID: {train.id} — Dep: {train.dep}</div>
            </div>
            <button onClick={onClose} className="px-2 py-1 bg-slate-200 rounded">Close</button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            <div>
              <div className="mb-2">Status: <b>{train.status}</b></div>
              <div className="mb-2">Route: {train.routeId ? routes.find((r) => r.id === train.routeId)?.name : '—'}</div>
              <div className="mb-2">Platform: {train.platform ?? '—'}</div>
              {pt && <div className="text-xs text-slate-500">Pos: {Math.round(pt.x)},{Math.round(pt.y)}</div>}
            </div>

            <div className="space-y-2">
              <div className="flex gap-2">
                <button onClick={() => markLate(train.id, 10)} className="px-3 py-1 bg-amber-300 rounded">Mark Late 10m</button>
                <button onClick={() => cancelTrain(train.id)} className="px-3 py-1 bg-red-400 text-white rounded">Cancel</button>
                <button onClick={() => clearStatus(train.id)} className="px-3 py-1 bg-slate-200 rounded">Reset</button>
              </div>
              <div className="text-sm">To assign from here, go to Assignments view and pick a platform and route.</div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <Nav />
      <main className="p-4">
        {view === "departure" && <DepartureBoard />}
        {view === "signaller" && <SignallerView />}
        {view === "assignments" && <AssignmentsView />}
        {view === "late" && <LateView />}
      </main>

      {selectedTrain && <TrainModal train={selectedTrain} onClose={() => setSelectedTrain(null)} />}
    </div>
  );
}
npm 