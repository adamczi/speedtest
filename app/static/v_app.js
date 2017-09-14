window.onload = function () {

    new Vue({
        el: '#speeds',
        data: {
            average: {},
            records: {}
        },
        methods: {
            setJson (payload) {
                var sum = 0;
                for (var i=0; i < payload.length; i++) {
                    sum += payload[i][1]
                };
                result = sum/i;
                this.average = Math.round(result * 1000) / 1000;
                this.records = i;
            },
        },

        delimiters: ['[[',']]'],
    });

}
