const generateButton = document.getElementById("GenEnc");
const encounterResult = document.getElementById("encounterResult");
const encounterResultNotHide = document.getElementById("encounterResultNotHide");


generateButton.addEventListener("click", async () => {
            try{
                const EncounterType = document.getElementById("EncounterType").value;
                const response = await fetch(`/generateEncounter?encType=${EncounterType}`);
                if(!response.ok)
                {
                    throw new Error("Could not get data");
                }
                const data = await response.json();
                document.getElementById("encounterDescription").textContent = data.description;
                document.getElementById("encounterType").textContent = EncounterType;
                document.getElementById("encounterTitle").textContent = data.title;
                document.getElementById("encounterTwist").textContent = data.twist;
                document.getElementById("encounterReward").textContent = data.reward;
                encounterResult.hidden = false;
                encounterResultNotHide.hidden = true;

            }catch(error){
                        console.error("Error:", error);
            }

            
            

});