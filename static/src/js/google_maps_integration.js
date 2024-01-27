var map;
var geocoder;
var marker = null;

function initialize() {
    var defaultLatitude = document.getElementById("latitude").value;
    var defaultLongitude = document.getElementById("longitude").value;

    if (defaultLatitude && defaultLongitude == 0) {
        defaultLatitude = -7.786566449336038;
        defaultLongitude = 110.39001459733059;
    }

    var mapOptions = {
        center: new google.maps.LatLng(defaultLatitude, defaultLongitude),
        zoom: 15,
        scrollwheel: true,
        disableDefaultUI: false,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };

    map = new google.maps.Map(document.getElementById("map_canvas"), mapOptions);
    geocoder = new google.maps.Geocoder();

    // Set the default marker
    setMarker(new google.maps.LatLng(defaultLatitude, defaultLongitude));

    map.addListener('click', function (e) {
        setMarker(e.latLng);

        var latLng = e.latLng.toJSON();
        console.log(latLng);
        document.getElementById("latitude").value = latLng.lat;
        document.getElementById("longitude").value = latLng.lng;

        // Get address from clicked location
        getAddress(e.latLng);
    });

    function setMarker(latLng) {
        if (!marker) {
            marker = new google.maps.Marker({
                position: latLng,
                map: map
            });
        } else {
            marker.setPosition(latLng);
        }
    }

    function getAddress(latLng) {
        geocoder.geocode({ 'location': latLng }, function (results, status) {
            if (status === 'OK') {
                if (results[0]) {
                    document.getElementById("lokasi").value = results[0].formatted_address;
                } else {
                    console.log('No results found');
                }
            } else {
                console.log('Geocoder failed due to: ' + status);
            }
        });
    }
}
