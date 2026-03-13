/**
 * ============================================================
 *  TEXTBOOK STORE — CONFIGURATION FILE
 *  Edit this file to update book images, titles, prices, etc.
 * ============================================================
 *
 *  FIELDS PER BOOK:
 *    image         → filename inside imageDir  (e.g. "bio.jpg")
 *    title         → full book title shown on invoice
 *    author        → author name(s)
 *    isbn          → ISBN-13
 *    year          → publishing year (number)
 *    price         → discounted / school price (number, no £ symbol)
 *    originalPrice → RRP / original price (number, no £ symbol)
 *
 *  TO ADD A NEW BOOK:
 *    1. Add a new entry in the "books" section below
 *    2. Place the cover image in your imageDir folder
 *    3. Use the same key in the "students" array if needed
 * ============================================================
 */

const STORE_CONFIG = {

  // ── General store settings ──────────────────────────────────
  storeName:     "Year 12 Books",
  currency:      "£",
  shippingCost:  3.00,
  shippingLabel: "Standard Shipping",

  // ── Image directory (trailing slash required) ────────────────
  //    Place all cover images in this folder next to index.html
  imageDir: "./img/",

  // ── Book catalogue ───────────────────────────────────────────
  books: {

    // ── MATHEMATICS ─────────────────────────────────────────────

    "AI SL": {
      image:         "aisl.jpg",
      title:         "Oxford IB Diploma Programme: IB Mathematics: Applications and Interpretation, Standard Level, Print and Enhanced Online Course Book Pack",
      author:        "Jane Forrest",
      isbn:          "978-0198426981",
      year:          2019,
      price:         62.39,
      originalPrice: 77.99
    },

    "AI HL": {
      image:         "aihl.jpg",
      title:         "Oxford IB Diploma Programme: IB Mathematics: Applications and Interpretation, Higher Level, Print and Enhanced Online Course Book Pack",
      author:        "Panayiotis Economopoulos",
      isbn:          "978-0198427049",
      year:          2019,
      price:         62.39,
      originalPrice: 77.99
    },

    "AA SL": {
      image:         "aasl.jpg",
      title:         "Oxford IB Diploma Programme: IB Mathematics: Analysis and Approaches, Standard Level, Print and Enhanced Online Course Book Pack",
      author:        "Paul La Rondie",
      isbn:          "978-0198427100",
      year:          2019,
      price:         62.39,
      originalPrice: 77.99
    },

    "AA HL": {
      image:         "aahl.jpg",
      title:         "Oxford IB Diploma Programme: IB Mathematics: Analysis and Approaches, Higher Level, Print and Enhanced Online Course Book Pack",
      author:        "Marlene Torres Skoumal",
      isbn:          "978-0198427162",
      year:          2019,
      price:         62.39,
      originalPrice: 77.99
    },


    // ── SCIENCES ─────────────────────────────────────────────────

    "Biology": {
      image:         "bio.jpg",
      title:         "Oxford Resources for IB DP Biology: Course Book",
      author:        "Oxford",
      isbn:          "978-1382016339",
      year:          2023,
      price:         49.59,
      originalPrice: 61.99
    },

    "Physics": {
      image:         "phy.jpg",
      title:         "Oxford Resources for IB DP Physics: Course Book",
      author:        "Oxford",
      isbn:          "978-1382016599",
      year:          2023,
      price:         49.59,
      originalPrice: 61.99
    },

    "Chemistry": {
      image:         "chem.jpg",
      title:         "Oxford Resources for IB DP Chemistry: Course Book",
      author:        "Oxford",
      isbn:          "978-1382016469",
      year:          2023,
      price:         49.59,
      originalPrice: 61.99
    },

    "ESS": {
      image:         "ess.jpg",
      title:         "Oxford Resources for IB DP Environmental Systems and Societies: Course Book",
      author:        "Oxford",
      isbn:          "978-1382044011",
      year:          2024,
      price:         48.44,
      originalPrice: 45.59
    },

    // ── HUMANITIES ───────────────────────────────────────────────

    "Global Politics": {
      image:         "glopo.jpg",
      title:         "Global Politics for the IB Diploma",
      author:        "",
      isbn:          "978-1036003500",
      year:          2024,
      price:         44.28,
      originalPrice: 54.00
    },

    "Economics": {
      image:         "econ.jpg",
      title:         "Economics for the IB Diploma",
      author:        "",
      isbn:          "978-1510479142",
      year:          2020,
      price:         47.56,
      originalPrice: 58.00
    },

    "Business": {
      image:         "busi.jpg",
      title:         "Business Management for the IB Diploma",
      author:        "Malcolm Surridge",
      isbn:          "978-1398350977",
      year:          2022,
      price:         47.56,
      originalPrice: 58.00
    },

    "History": {
      image:         "hist.jpg",
      title:         "History for the IB Diploma",  // ← update title/ISBN when available
      author:        "",
      isbn:          "",      // ← fill in
      year:          null,    // ← fill in
      price:         39.99,   // ← fill in
      originalPrice: null     // ← fill in
    },

    "Psychology": {
      image:         "psych.jpg",
      title:         "Oxford Resources for IB DP Psychology: Course Book",
      author:        "Oxford",
      isbn:          "978-1382056663",
      year:          2025,
      price:         39.99,
      originalPrice: 49.99
    },

    // ── GROUP F / ADDITIONAL ─────────────────────────────────────

    "Computer Science": {
      image:         "cs.jpg",
      title:         "Oxford Resources for IB DP Computer Science: Course Book",
      author:        "Oxford",
      isbn:          "978-1382063920",
      year:          2025,
      price:         41.59,
      originalPrice: 51.99   // ← note: originalPrice is lower than discounted; confirm if correct
    },

    "Spanish B": {
      image:         "spa.jpg",
      title:         "IB Spanish B Course Book Pack: Oxford IB Diploma Programme (Print Course Book & Enhanced Online Course Book)",
      author:        "Ana Valbuena",
      isbn:          "978-0198422426",
      year:          2018,
      price:         52.79,
      originalPrice: 65.99
    },

    "French B": {
      image:         "fre.jpg",
      title:         "IB French B Course Book Pack: Oxford IB Diploma Programme (Print Course Book & Enhanced Online Course Book)",
      author:        "Christine Trumper",
      isbn:          "978-0198422372",
      year:          2018,
      price:         52.79,
      originalPrice: 65.99
    },

    "Visual Arts": {
      image:         "va.jpg",
      title:         "Oxford Resources for IB DP Visual Arts: Course Book",
      author:        "Oxford",
      isbn:          "978-1382060660",
      year:          2025,
      price:         30.79,
      originalPrice: 38.49
    },

    "Arts": {  // alternate key used in student data — mirrors Visual Arts
      image:         "va.jpg",
      title:         "Oxford Resources for IB DP Visual Arts: Course Book",
      author:        "Oxford",
      isbn:          "978-1382060660",
      year:          2025,
      price:         30.79,
      originalPrice: 38.49
    }

  }, // end books


  // ── Student → subject mapping ────────────────────────────────
  // Format: [Math, Science, Humanities, Group F]
  // Use "" for an empty slot (student has no book in that group).
  students: [
    ["AI SL",  "Biology",  "Business",         "Spanish B"      ],
    ["AI SL",  "Biology",  "Global Politics",  "Chemistry"      ],
    ["AI HL",  "Physics",  "Business",         "Computer Science"],
    ["AA SL",  "Biology",  "Business",         "Spanish B"      ],
    ["AA HL",  "Physics",  "Business",         "Computer Science"],
    ["AI SL",  "Biology",  "Business",         "Arts"           ],
    ["AI SL",  "Biology",  "Business",         "Chemistry"      ],
    ["AA HL",  "Physics",  "Global Politics",  "Computer Science"],
    ["AA HL",  "Physics",  "History",          "Computer Science"],
    ["AI SL",  "Biology",  "Business",         "French B"       ],
    ["AA HL",  "ESS",      "Economics",        "Computer Science"],
    ["AA SL",  "Biology",  "Business",         "Chemistry"      ],
    ["AA HL",  "Physics",  "Economics",        "Computer Science"],
    ["AI SL",  "Biology",  "Business",         "Psychology"     ],
    ["AA SL",  "ESS",      "Business",         "Computer Science"],
    ["AA Hl",  "ESS",      "Economics",        ""               ],
    ["AA HL",  "Physics",  "Global Politics",  "Spanish B"      ],
    ["AI SL",  "Physics",  "Business",         "Computer Science"],
    ["AI SL",  "Biology",  "Business",         "Arts"           ],
    ["AI SL",  "Biology",  "Psychology",       "Arts"           ],
    ["AI HL",  "Physics",  "Business",         "Computer Science"],
    ["AI SL",  "ESS",      "Business",         "Visual Arts"    ],
    ["AA HL",  "Physics",  "Global Politics",  "Computer Science"],
    ["AI SL",  "Biology",  "Global Politics",  "Arts"           ],
    ["AI SL",  "Biology",  "Global Politics",  "French B"       ],
    ["AI SL",  "Biology",  "Global Politics",  "French B"       ]
  ]

};
