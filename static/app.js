/**
 * Created by eukeni on 04/12/16.
 */

var app = angular.module('RugerHydro', ['ui.router']);

app
    .config(['$urlRouterProvider', '$stateProvider', function($urlRouterProvider, $stateProvider) {
        $urlRouterProvider.otherwise('/');

        $stateProvider.state('/', {
            url: '/',
            templateUrl: '/static/templates/home.html',
            controller: 'IndexCtrl'
        });
        $stateProvider.state('/data', {
            url: '/data',
            templateUrl: '/static/templates/data.html',
            controller: 'DataCtrl',
            resolve:{
                data: ['$http', '$q', function($http, $q){
                    var promise = $q.defer();
                    promise.resolve($http.get('/api/query').then(function(response){
                        return response.data;
                    }));
                    return promise.promise;
                }]
            }
        });
        $stateProvider.state('/settings', {
            url: '/settings',
            templateUrl: '/static/templates/settings.html',
            controller: 'SettingsCtrl'
        });
        $stateProvider.state('/config', {
            url: '/config',
            templateUrl: '/static/templates/config.html',
            controller: 'ConfigCtrl',
            resolve: {
                sensors: ['$http', '$q', function($http, $q){
                    var promise = $q.defer();
                    promise.resolve($http.get('/api/get_custom_sensor').then(function(response){
                        return response.data.sensors;
                    }));
                    return promise.promise;
                }],
                data_types: ['$http', '$q', function($http, $q){
                    var promise = $q.defer();
                    promise.resolve($http.get('/api/get_data_types').then(function(response){
                        return response.data.types;
                    }));
                    return promise.promise;
                }]
            }
        });
    }]);