window.onload = function () {
    document.getElementById("historical").src = "https://api.maptiler.com/tiles/uk-osgb1919/?key=" + key + "#6.7/57.26352/-4.20261"
}
streetKey = "{{MAPS_KEY}}"
document.getElementById("map_trigger").addEventListener('click', function () {
    const address = document.getElementById("address").value
    console.log(address)

    fetch(`https://maps.googleapis.com/maps/api/geocode/json?address=${address}&key=${streetKey}`)
        .then((response) => {
            return response.json()
        }).then(data => {
            document.getElementById("streetview").style = "display: block;";
            document.getElementById("streetview").setAttribute("src", "https://www.google.com/maps/embed/v1/streetview?key=" + streetKey + "&location=" + data.results[0].geometry.location['lat'] + "," + data.results[0].geometry.location['lng'] + "&heading=210&pitch=10&fov=35");
            document.getElementById("address").value = "";
        }).catch(error => {
            console.log(error)
        })
})
