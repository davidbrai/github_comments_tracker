
var app = angular.module('comments', ['threads']).config(function($routeProvider) {
    $routeProvider.when('/', {
        controller:CommentsCtrl, templateUrl:'/static/js/templates/comments-view.html'
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

function CommentsCtrl($scope, Thread) {
    $scope.threads = Thread.query();
}