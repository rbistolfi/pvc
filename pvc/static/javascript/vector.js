// vector.js
// Angular controller for Vector Packages
// rbistolfi


function VectorPackagesController ($scope, $routeParams, $http) {
    
    $scope.page = 1;
    $scope.category = 0;
    $scope.items_per_page = 12;

    var api_url = '/api/1/package/?sort=[("name",1)]&page=1&max_results='+$scope.items_per_page;

    var featured = [
	"UrbanTerror", "KoboDeluxe", "0ad",
	"blender", "minitube", "libreoffice",
	"vlc", "xbmc", "celestia",
	"node", "redis", "scratch",
    ];

    function get_packages (api_url, func) {
	$("#vector-loader").addClass("active");
	$http.get(api_url).
	    success(function(data, status, header, config) {
	    func(data, status, header, config);
		$("#vector-loader").removeClass("active");
	    }).
	    error(function (err) {
		alert(err);
		$("#vector-loader").removeClass("active");
	    });
    }

    function set_packages (data) {
	$scope.packages = data._items;
	$scope.links = data._links;
    }

    $scope.all_packages = function() {
	get_packages(api_url, set_packages);
	$scope.page = 1;
	$scope.category = 0;
    }

    $scope.set_category = function (i) {
	if ($scope.category === i) {
	    return;
	}
	if (i == 9) {
	    $scope.packages = [];
	    $scope.category = i;
	    $scope.links = null;
	    for (i in featured) {
		var url = api_url+'&where=name=="'+featured[i]+'"';
		$http.get(url).success(function (data) {
		    $scope.packages.push(data._items[0]);
		});
	    }
	}
    }

    $scope.search = function (keyword) {
	keyword = encodeURIComponent(keyword);
	var search_url = api_url+'&where=name=="'+keyword+'"';
	get_packages(search_url, set_packages);
	$scope.query = "";
	$scope.category = 8;
    }

    $scope.next_page = function () {
	var page_url = $scope.links.next.href;
	get_packages(page_url, set_packages);
	$scope.page++;
	$("body,html").animate({scrollTop: 0}, "slow");
    }

    $scope.previous_page = function () {
	var page_url = $scope.links.prev.href;
	get_packages(page_url, set_packages);
	$scope.page--;
	$("body,html").animate({scrollTop: 0}, "slow");
    }

    //$scope.set_category(9);
    get_packages(api_url, set_packages);

}


function PackageDetailController ($scope, $routeParams, $http) {
    $scope.name = $routeParams.pkgname;
    window.disqus_identifier = $scope.name;
    var api_url = '/api/1/package/?sort=[("name", 1)]&page=1&max_results=12';
    var name = encodeURIComponent($scope.name);
    var url = api_url+'&where=name=="'+name+'"';
    $http.get(url).
	success(function(data, status, header, config) {
	    $scope.app = data._items[0];
	}).
	error(function (err) {
	    alert(err);
	});
}


var vector_module = angular.module("vector", []);
 
     
vector_module.directive('findImageFor', function factory ($http) {
    return {
	restrict: "EAC",
	link: function (scope, element, attrs) {
	    scope.$watch("findImageFor", function() {
		var snd_src = "https://sigil.cupcake.io/"+attrs.findImageFor;
		var alt = attrs.findImageFor;
		var url = "https://ajax.googleapis.com/ajax/services/search/images"+
		    "?callback=JSON_CALLBACK&v=1.0&safe=active&imgsz=medium&q="+alt;
		$http.jsonp(url, {cache: true}).
		    success(function(result) {
			console.log(result);
			var src = result.responseData.results[0].unescapedUrl;
			var img = '<img height=250 src="'+src+'">';
			element.append(img);
		    }).
		    error(function (err) {
			console.log(err);
			var img = '<img src="'+snd_src+'">';
			element.append(img);
		    });
	    });
	}
    }
});


vector_module.config(['$routeProvider', function ($routeProvider) {
    $routeProvider.
	when('/', {controller: VectorPackagesController, templateUrl: "/p/static/partials/package-list.html"}).
	when('/:pkgname', {controller: PackageDetailController, templateUrl: "/p/static/partials/package-detail.html"}).
	otherwise({redirectTo: '/'});
}]);


vector_module.filter("deplist", function () {
    return function (text) {
        if (text) {
	    var new_dep = [];
	    var deps = text.split(",");
	    for (i in deps) {
		var name = deps[i].split(" ")[0];
		new_dep.push(name);
	    }
	    return new_dep.join(", ");
	}
	return "None"
    }
});


//PackageDetailController.$inject = ['$scope', '$routeParams', '$html']; 
//VectorPackagesController.$inject = ['$scope', '$routeParams', '$html']; 
