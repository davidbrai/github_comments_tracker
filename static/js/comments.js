
var app = angular.module('comments', ['threads', 'repos']).config(function($routeProvider) {
    $routeProvider.when('/mine/:repoid', {
        controller:MyThreadsCtrl, templateUrl:'/static/js/templates/comments-view.html'
    }).when('/all/:repoid', {
        controller:AllThreadsCtrl, templateUrl:'/static/js/templates/comments-view.html'
    }).otherwise({
        redirectTo:'/mine/'
    });
});

angular.module('comments').
    filter('fromNow', function() {
        return function(dateString) {
            return moment(new Date(dateString)).fromNow()
        };
    });

function AllThreadsCtrl($scope, Threads, Repos) {
    $scope.mode = 'all';
    $scope.threads = Threads.all.query();
    $scope.repos = Repos.all.query();
}

function MyThreadsCtrl($scope, Threads, Repos) {
    $scope.mode = 'mine';
    $scope.threads = Threads.mine.query();
    $scope.unreadFilter = {read: 'false'};
    $scope.markAsRead = Threads.markAsRead;
    $scope.repos = Repos.all.query();
}