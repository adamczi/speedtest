window.onload = function () {

    var numbers = Vue.component('numbers', {
        props: ['table'],

        data: function () {
            var sum = 0;
            for (var i=0; i < this.table.length; i++) {
                sum += this.table[i][1]
            };
            var result = Math.round(sum/i * 1000) / 1000;

            return {
                average: result,
                count: i,
                firstDate: {}, //compute max and min of this.table's timestamps
                lastDate: {}
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


    var app = new Vue ({
        el: '#speeds',
        delimiters: ['[[',']]']
    });
}
