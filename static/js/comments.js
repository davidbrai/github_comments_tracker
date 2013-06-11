
var app = angular.module('comments', ['threads']).config(function($routeProvider) {
    $routeProvider.when('/', {
        controller:MyThreadsCtrl, templateUrl:'/static/js/templates/comments-view.html'
    }).when('/all', {
        controller:AllThreadsCtrl, templateUrl:'/static/js/templates/comments-view.html'
    }).otherwise({
        redirectTo:'/'
    });
});

angular.module('comments').
    filter('fromNow', function() {
        return function(dateString) {
            return moment(new Date(dateString)).fromNow()
        };
    });

function AllThreadsCtrl($scope, Threads) {
    $scope.mode = 'all';
    $scope.threads = Threads.all.query();
    $scope.markAsRead = Threads.markAsRead;
}

function MyThreadsCtrl($scope, Threads) {
    $scope.mode = 'mine';
    $scope.threads = Threads.mine.query();
    $scope.markAsRead = Threads.markAsRead;
}