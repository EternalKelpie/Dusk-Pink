function downloadJson(data, filename){

    var json =JSON.stringify(data);

    var blob = new Blob([json], {type: 'application/json'});

    var url = URL.createObjectURL(blob);

    var link = document.createElement('a');
    link.setAttribute('download', filename);

    link.href = url;

    document.body.appendChild(link);
    link.click();

    document.body.removeChild(link);
    URL.revokeObjectURL(url);
}

function GetMap(data, map ){
     const mapElementFinal = document.createElement("div");
        mapElementFinal.className = "dungeonMap";

        const mapLen =40;
        const mapHei = 30;

        mapElementFinal.style.gridTemplateColumns= 
        `repeat(${mapLen}, 16px )`;


            for (const row of data.map){
                for(const cell of row){
                    const tile = document.createElement("div");
                    tile.className = `tile ${cell === 0 ? "floor" : "wall"}`;
                    mapElementFinal.appendChild(tile);

                }


            }

        mapElementFinal.style.display = "grid";
        mapElementFinal.style.gridTemplateColumns = `repeat(${mapLen}, 16px)`;
        mapElementFinal.style.gridAutoRows = "16px";
        mapElementFinal.style.gap = "1px";
        mapElementFinal.style.textAlign = "center";
        mapElementFinal.style.margin = "0 auto";

            mapElementFinal.querySelectorAll(".tile").forEach(tile => {
                tile.style.width = "16px";
                tile.style.height = "16px";
                tile.style.display = "block";

                if(tile.classList.contains("wall"))
                {
                    tile.style.backgroundColor = "#141239";
                }
                else if (tile.classList.contains("floor"))
                {
                    tile.style.backgroundColor = "#006d46";
                }

            });

        const tiles = mapElementFinal.querySelectorAll(".tile");

            tiles.forEach(tile => {
                tile.style.width = "16px";
                tile.style.height = "16px";
            });
            map.replaceChildren(mapElementFinal);

}



const map = document.getElementById("map");
const button = document.getElementById("mainDunBut");

button.addEventListener("click", () =>{

    //first display the grid for map  

    const mapElement = document.createElement("div");
    mapElement.className = "dungeonMap";

    const mapLen =40;
    const mapHei = 30;

    mapElement.style.gridTemplateColumns= 
    `repeat(${mapLen}, 16px )`;

        for (let y = 0; y < mapHei; y++)
        {for (let x =0; x < mapLen; x++)
        {
            const tile = document.createElement("div");
            tile.className = "tile wall";
            mapElement.appendChild(tile);
        }
        }

    mapElement.style.display = "grid";
    mapElement.style.gridTemplateColumns = `repeat(${mapLen}, 16px)`;
    mapElement.style.gridAutoRows = "16px";
    mapElement.style.gap = "1px";
    map.style.textAlign = "center";
    mapElement.style.margin = "0 auto";

        mapElement.querySelectorAll(".tile").forEach(tile => {
            tile.style.width = "16px";
            tile.style.height = "16px";
            tile.style.backgroundColor = "lime";
            tile.style.display = "block";
        });

    const tiles = mapElement.querySelectorAll(".tile");

        tiles.forEach(tile => {
            tile.style.width = "16px";
            tile.style.height = "16px";
        });
        map.replaceChildren(mapElement);

    map.style.display = "flex";
    map.style.justifyContent = "center";

    mapElement.style.margin = "0";
    mapElement.style.flexShrink = "0";

    // here is saving
    const saveMapButton =document.getElementById("SaveMapButton");
  

    saveMapButton.addEventListener("click", async () =>{
      try{
            const response = await fetch(`/load`);

            if(!response.ok)
            {
                console.error("Could not fetch file");
                return;
            }

            const jsonMapData = await response.json();

            downloadJson(jsonMapData, "map.json");

        } catch(error) {
            console.error("Error with saving map");
        }

    });

    //here is loading
    const loadButton =document.getElementById("LoadMapButton");
    const exterMap = document.getElementById("exterMap");
    loadButton.addEventListener("click", async () =>{
            const file = exterMap.files[0];


            if(!file)
            {
                console.error("Error with loading map", error);
                return;
            }
        try {
                const text =await file.text();
                const data = JSON.parse(text);

                if(!Array.isArray(data.map) || !data.map.every(row =>Array.isArray(row)))
                {

                    throw new Error("File does not contain map.");
                }
            

            GetMap(data, map );

        } catch (error) {
                console.error("Error with map generation:", error);
            }
    });
    


    const genButton =document.getElementById("genButton");
    //map generation
    genButton.addEventListener("click", async () =>{
    const RoomNumber = document.getElementById("rnum");
    const roomCount = Number(RoomNumber.value);

    const Loot = document.getElementById("lootSwitch");
    const Encounter = document.getElementById("EncSwitch");

    try {

        if(Loot.checked && Encounter.checked)
        {
            console.log("add generating loot and enc..");
        }
        const response = await fetch(`/generate?rooms=${roomCount}`);

        if (!response.ok) {
                throw new Error("Could not get map.");
        }
    
        const data = await response.json();

        GetMap(data, map);

    } catch (error) {
        console.error("Error with map generation:", error);
    }

    });


});
