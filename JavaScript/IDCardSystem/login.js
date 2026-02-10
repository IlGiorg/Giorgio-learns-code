const form = document.getElementById("loginform");
    form.addEventListener("submit",function(event){
        event.preventDefault();
        const username=document.getElementById=("userinput").value;
        const password=document.getElementById=("passinput").value;   
        if (username === "secretuser"){
            document.getElementById("outcome").innerText = "success"
        }
        else{
            document.getElementById("outcome").innerText="Wrong Password"
        }
           
    });