odoo.define('your_module_name.project_form', function (require) {
    "use strict";

    var core = require('web.core');
    var FormView = require('web.FormView');
    var rpc = require('web.rpc');

    var _t = core._t;

    FormView.include({
        map: null, // Store the map instance

        render: function () {
            this._super.apply(this, arguments);
            this.$('.o_form_view').on('click', '.o_google_map_marker', this._onMapMarkerClick.bind(this));

            // Add a click event listener to the map container
            this.$('#googleMap').on('click', this._onMapClick.bind(this));

            // Initialize the map and store the instance
            this.map = this._initMap();
        },

        _initMap: function () {
            var mapProp = {
                center: new google.maps.LatLng(51.508742, -0.120850),
                zoom: 5,
            };
            return new google.maps.Map(document.getElementById("googleMap"), mapProp);
        },

        _onMapClick: function (ev) {
            var map = this.map;
            var latLng = ev.latLng;

            // Create a marker at the clicked location
            var marker = new google.maps.Marker({
                position: latLng,
                map: map,
                title: 'New Marker',
            });

            // Update the latitude and longitude fields in the form
            this.$('input[name="latitude"]').val(latLng.lat());
            this.$('input[name="longitude"]').val(latLng.lng());
        },

        _onMapMarkerClick: function (ev) {
            var $marker = $(ev.currentTarget);
            var latitude = $marker.data('latitude');
            var longitude = $marker.data('longitude');

            // Do something with the marker information, e.g., show a popup or navigate to a related record.
            // You can use Odoo's RPC to perform additional actions based on the marker information.
        },
    });
});
