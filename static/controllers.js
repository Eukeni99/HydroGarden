/**
 * Created by eukeni on 04/12/16.
 */

app
    .controller('DataCtrl', ['$scope', 'data', function($scope, data){
        $scope.items = data.data;
        $scope.headers = data.headers;
        $scope.render_date = function (date, time) {
            return moment(date + ' ' + time, 'DD/MM/YYYY HH:mm:ss').format('DD/MM/YYYY HH:mm:ss');
        }
    }])
    .controller('IndexCtrl', ['$scope', function ($scope) {
        
    }])
    .controller('SettingsCtrl', ['$scope', function ($scope) {
        
    }])
    .controller('ConfigCtrl', ['$scope', '$http', 'sensors', 'data_types', function ($scope, $http, sensors, data_types) {
        $scope.sensors = sensors;
        $scope.data_types = data_types;
        console.log($scope.data_types);
        $scope.post_data = function(){
            $http.post('/api/save_custom_sensors', $scope.sensors)
        }
    }]);