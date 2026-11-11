const returnButton = document.getElementById("backButton");

returnButton.addEventListener("click",  () =>{
    window.location.href ="/"; 
});

const createButton = document.getElementById("createButton");

createButton.addEventListener("click", async () =>{
const name = document.getElementById("name").value;
const race = document.getElementById("race").value;
const job = document.getElementById("job").value;
const looks = document.getElementById("looks").value;
const act = document.getElementById("act").value;

try{
 const response = await fetch(`/saveNpcToJson?name=${name}&race=${race}&job=${job}&looks=${looks}&act=${act}`);

    if (!response.ok) {
                throw new Error("Could save.");
        }
}catch (error) {
        console.error("Error with saving to database:", error);
}
    window.location.href = "/#mainCharBut";
});



