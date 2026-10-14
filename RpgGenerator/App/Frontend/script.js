const map = document.getElementById("map");
const button = document.getElementById("mainDunBut");

button.addEventListener("click", () =>{
const mapElement = document.createElement("div");
mapElement.className = "dungeonMap";

const mapLen =40;
const mapHei = 30;

mapElement.style.gridTemplateColumns= 
`repeat(${mapLen}, 16 px )`;

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


});

