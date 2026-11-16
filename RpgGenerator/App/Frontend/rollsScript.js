function rollDice( max){
const number = Math.floor(Math.random() * max) +1;
document.getElementById("RollResult").textContent = number.toString();

}

const k4 = document.getElementById("k4");
const k6 = document.getElementById("k6");
const k8 = document.getElementById("k8");
const k10 = document.getElementById("k10");
const k12 = document.getElementById("k12");
const k20 = document.getElementById("k20");
const k100 = document.getElementById("k100");
const custom = document.getElementById("rollCusotomDiceButton");


k4.addEventListener("click",  () =>{rollDice(4)});
k6.addEventListener("click",  () =>{rollDice(6)});
k8.addEventListener("click",  () =>{rollDice(8)});
k10.addEventListener("click",  () =>{rollDice(10)});
k12.addEventListener("click",  () =>{rollDice(12)});
k20.addEventListener("click",  () =>{rollDice(20)});
k100.addEventListener("click",  () =>{rollDice(100)});

custom.addEventListener("click",  () =>{
    try{
    const diceType = Number(document.getElementById("diceType").value);
    const diceNumber = Number(document.getElementById("diceNumber").value);
    let result = 0;
     for (let i=0; i<diceNumber; i++)
     {
        result+= Math.floor(Math.random() * diceType) +1;
     }
        document.getElementById("RollResult").textContent = result.toString();

    }catch {console.error("Not a number");}


});