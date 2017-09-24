window.onload = function () {
var a = performance.now();

// utilities
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


// Component for viewing speed data (top right)
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

// Component for viewing dates (top left)
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


// Component for the last IP/ISP data (bottom left and right)
    var isp = Vue.component('isp', {
        data: function() {
            return {
                ips: this.$parent.cacheTables[3],
                providers: this.$parent.cacheTables[4]
            }
        },
        computed: {
            name: function () {
                let l = this.providers.length-1;
                return this.providers[l][1];
            },
            ip: function () {
                let l = this.ips.length-1;
                return this.ips[l][1];
            }
        }
    })
// Extensions of above isp component
    var ispName = isp.extend({
        template: '<p>ISP: {{name}}</p>'
    })
    Vue.component('isp-name', ispName)

    var ip = isp.extend({
        template: '<p>IP: {{ip}}</p>'
    })
    Vue.component('ip', ip)


// Component for table tab
    var valuetable = Vue.component('valuetable', {
        data: function () {
            let downloads = this.$parent.cacheTables[0];
            let uploads = this.$parent.cacheTables[1];
            let pings = this.$parent.cacheTables[2];
            let tabledata = [];

            for (let i = 0; i < downloads.length; i++) {
                // Convert date to ISO format
                let d = new Date(downloads[i][0]).toISOString();
                tabledata.push({
                    key: i+1,
                    value: [d,
                            downloads[i][1],
                            uploads[i][1],
                            pings[i][1]]
                })
            }
            // Show only last 5 records
            if (tabledata.length > 5) {
                tabledata = tabledata.slice(-5)
            }

            return {
                tabledata: tabledata
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
                        <tr v-for="item in tabledata">\
                            <td>{{item.key}}</td>\
                            <td>{{item.value[0]}} </td>\
                            <td>{{item.value[1]}} </td>\
                            <td>{{item.value[2]}} </td>\
                            <td>{{item.value[3]}} </td>\
                        </tr>\
                    </tbody>\
                  </table>'
    })

// The main Vue app
    var app = new Vue ({
        delimiters: ["<%","%>"],
        el: '#speeds',
        data: {
            cacheTables: null
        },
        beforeMount: function () {
            // Get Flask data from div attribute
            this.cacheTables = this.$el.attributes['my-data'].value;
            this.cacheTables = JSON.parse(this.cacheTables.replace(/'/g, '"'));
        },

    });

var b = performance.now();
// alert('It took ' + (b - a) + ' ms.');

}
