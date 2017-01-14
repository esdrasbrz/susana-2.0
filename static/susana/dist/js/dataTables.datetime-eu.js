jQuery.extend( jQuery.fn.dataTableExt.oSort, {
    "datetime-eu-pre": function ( date ) {
        var time = date.replace(" ", "").substr(12, 5).split(/\:/);
        date = date.replace(" ", "").substr(0, 10);

        if ( ! date ) {
            return 0;
        }

        var year;
        var eu_date = date.split(/[\.\-\/]/);

        /*year (optional)*/
        if ( eu_date[2] ) {
            year = eu_date[2];
        }
        else {
            year = 0;
        }

        /*month*/
        var month = eu_date[1];
        if ( month.length == 1 ) {
            month = 0+month;
        }

        /*day*/
        var day = eu_date[0];
        if ( day.length == 1 ) {
            day = 0+day;
        }

        var hour = time[0];
        var minute = time[1];

        return (year + month + day + hour + minute) * 1;
    },

    "datetime-eu-asc": function ( a, b ) {
        return ((a < b) ? -1 : ((a > b) ? 1 : 0));
    },

    "datetime-eu-desc": function ( a, b ) {
        return ((a < b) ? 1 : ((a > b) ? -1 : 0));
    }
} );
