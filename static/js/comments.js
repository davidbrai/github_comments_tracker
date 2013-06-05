
var app = angular.module('comments', ['threads']).config(function($routeProvider) {
    $routeProvider.when('/', {
        controller:CommentsCtrl, templateUrl:'/static/js/templates/comments-view.html'
    }).otherwise({
        redirectTo:'/'
    });
});

function CommentsCtrl($scope, Thread) {
    $scope.threads = Thread.query();
}