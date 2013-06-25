
var app = angular.module('comments', ['threads']).config(function($routeProvider) {
    $routeProvider.when('/', {
        controller:MyThreadsCtrl, templateUrl:'/static/js/templates/comments-view.html'
    }).when('/all', {
        controller:AllThreadsCtrl, templateUrl:'/static/js/templates/comments-view.html'
    }).otherwise({
        redirectTo:'/'
    });
});

angular.module('comments').filter('fromNow', function() {
    return function(dateString) {
        return moment(new Date(dateString)).fromNow()
    };
});

angular.module('comments').filter('markdown', function() {
    var converter = new Showdown.converter();
    return function(markdownString) {
        return converter.makeHtml(markdownString);
    }
});

angular.module('comments').filter('escapeHtml', function() {
    return function(text) {
        if (text) {
            return text.
                replace(/&/g, '&amp;').
                replace(/</g, '&lt;').
                replace(/>/g, '&gt;');
        }
        return '';
    }
});

function AllThreadsCtrl($scope, Threads) {
    $scope.mode = 'all';
    $scope.threads = Threads.all.query();
}

function MyThreadsCtrl($scope, Threads) {
    $scope.mode = 'mine';
    $scope.threads = Threads.mine.query();
    $scope.unreadFilter = {read: 'false'};
    $scope.markAsRead = Threads.markAsRead;
}