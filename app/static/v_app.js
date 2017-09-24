window.onload = function () {
var a = performance.now();

    var computeAverage = function(data) {
        let sum = 0;
        for (var i=0; i < data.length; i++) {
            sum += data[i][1]
        };
        let average = Math.round(sum/i * 1000) / 1000;

        return average;
    }


    var computeDates = function(data) {
        let firstDate = lastDate = 0;
        for (let i=0; i < data[0].length; i++) {
            if (data[i][0] < firstDate || firstDate === 0) {
                firstDate = data[i][0];
            };
            if (data[i][0] > lastDate || lastDate === 0) {
                lastDate = data[i][0];
            };
        };
        let fd = new Date(firstDate);
        let ld = new Date(lastDate);
        return [String(fd), String(ld)];
    }


// Main component for speed data and date and it's extensions
    var numbers = Vue.component('numbers', {
        data: function () {
            return {
                downloads: this.$parent.cacheTables[0],
                uploads: this.$parent.cacheTables[1],
                pings: this.$parent.cacheTables[2]
            }
        },

        computed: {

            download: function() {
                return computeAverage(this.downloads);
            },

            upload: function() {
                return computeAverage(this.uploads);
            },

            ping: function() {
                return computeAverage(this.pings);
            }
        },
        template:  '<div><p>download: {{download}}</p>\
                    <p>upload: {{upload}}</p>\
                    <p>ping: {{ping}}</p></div>'
    })


    var dates = Vue.component('dates', {
        data: function () {
            return {
                records: this.$parent.cacheTables[0]
            }
        },

        computed: {

            count: function() {
                return this.records.length;
            },

            firstDate: function () {
                return computeDates(this.records)[0];
            },

            lastDate: function() {
                return computeDates(this.records)[1];
            }
        },
        template:  '<div><p>records total: {{count}}</p>\
                    <p>first record: {{firstDate}}</p>\
                    <p>last record: {{lastDate}}</p></div>'

    })


    // Component for IP/ISP data and extensions
    var isp = Vue.component('isp', {
        data: function() {
            return {
                IspIp: this.$parent.cacheTables[3]
            }
        },
        computed: {
            // props: ['isp'],
            name: function () {
                return this.IspIp[1];
            },
            ip: function () {
                return this.IspIp[0];
            }
        }
    })

    var ispName = isp.extend({
        template: '<p>ISP: {{name}}</p>'
    })
    Vue.component('isp-name', ispName)

    var ip = isp.extend({
        template: '<p>IP: {{ip}}</p>'
    })
    Vue.component('ip', ip)



    var valuetable = Vue.component('valuetable', {
        data: function () {
            return {
                downloads: this.$parent.cacheTables[0],
                uploads: this.$parent.cacheTables[1],
                pings: this.$parent.cacheTables[2]
            }
        },
        template: '<table class="table table-striped table-hover ">\
                    <thead>\
                        <tr>\
                          <th>#</th>\
                          <th>date</th>\
                          <th>download</th>\
                          <th>upload</th>\
                          <th>ping</th>\
                        </tr>\
                    </thead>\
                          \
                      <tbody>\
                        <tr v-for="item in downloads">\
                            <td>1</td>\
                            <td>{{item[0]}} </td>\
                            <td>{{item[1]}} </td>\
                            <td>{{item[1]}} </td>\
                            <td>{{item[1]}} </td>\
                        </tr>\
                    </tbody>\
                  </table>'
    })



    var app = new Vue ({
        delimiters: ["<%","%>"],
        el: '#speeds',
        data: {
            cacheTables: null
        },
        beforeMount: function () {
            this.cacheTables = this.$el.attributes['my-data'].value;
            this.cacheTables = JSON.parse(this.cacheTables.replace(/'/g, '"'));
        },

    });

var b = performance.now();
// alert('It took ' + (b - a) + ' ms.');

}
