
var app = angular.module('comments', ['threads', 'repos']).config(function($routeProvider) {
    $routeProvider.when('/:mode/:repoid', {
        controller:ThreadsCtrl, templateUrl:'/static/js/templates/comments-view.html'
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

function ThreadsCtrl($scope, $routeParams, Threads, Repos) {
    $scope.mode = $routeParams.mode;
    $scope.active_repo_id = $routeParams.repoid;
    $scope.repos = Repos.all.query();

    if ($scope.mode == 'mine') {
        $scope.threads = Threads.mine.query();
        $scope.unreadFilter = {read: 'false'};
        $scope.markAsRead = Threads.markAsRead;
    } else {
        $scope.threads = Threads.all.query();
    }
}