
var app = angular.module('comments', []).config(function($routeProvider) {
    $routeProvider.when('/', {
        controller:CommentsCtrl, templateUrl:'/static/js/templates/comments-view.html'
    }).otherwise({
        redirectTo:'/'
    });
});

function CommentsCtrl($scope) {
    $scope.comments = [{body:'fu'}];
}