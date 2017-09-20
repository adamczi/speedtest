window.onload = function () {


// Main component for speed data and date and it's extensions
    var numbers = Vue.component('numbers', {
        props: ['table'],

        data: function () {
            firstDate = 0;
            lastDate = 0;
            var sum = 0;
            for (var i=0; i < this.table.length; i++) {
                sum += this.table[i][1]
                if (this.table[i][0] < firstDate || firstDate === 0) {
                    firstDate = this.table[i][0];
                };
                if (this.table[i][0] > firstDate || lastDate === 0) {
                    lastDate = this.table[i][0];
                };
            };

            var fd = new Date(firstDate);
            var ld = new Date(lastDate);
            var result = Math.round(sum/i * 1000) / 1000;

            return {
                average: result,
                count: i,
                firstDate: String(fd),
                lastDate: String(ld)
            };
        }
    })


    var numbersaverage = numbers.extend({
        template: '<span>{{average}}</span>'
    })
    Vue.component('numbersaverage', numbersaverage)


    var numberscount = numbers.extend({
        template: '<span>{{count}}</span>'
    })
    Vue.component('numberscount', numberscount)


    var firstdate = numbers.extend({
        template: '<span>{{firstDate}}</span>'
    })
    Vue.component('firstdate', firstdate)


    var lastdate = numbers.extend({
        template: '<span>{{lastDate}}</span>'
    })
    Vue.component('lastdate', lastdate)



    // Component for IP/ISP data and extensions
    var isp = Vue.component('isp', {
        props: ['ispdata'],

        data: function () {
                return {
                    ip: this.ispdata[0],
                    name: this.ispdata[1]
        }
    }
    })

    var ispName = isp.extend({
        template: '<span>{{name}}</span>'
    })
    Vue.component('isp-name', ispName)

    var ip = isp.extend({
        template: '<span>{{ip}}</span>'
    })
    Vue.component('ip', ip)


    var app = new Vue ({
        el: '#speeds',
        delimiters: ['[[',']]']
    });
}
