(function() {
  describe("MyCtrl2", function() {
    beforeEach(module("app"));
    beforeEach(inject(function($rootScope, $controller) {
      var ctrl, scope;
      scope = $rootScope.$new();
      return ctrl = $controller("MyCtrl2", {
        $scope: scope,
        version: "9.9.9"
      });
    }));
    it("should be injected correctly", function() {
      expect(ctrl).not.to.be(void 0);
      return expect(scope.people.length).to.be(3);
    });
    describe("longestName computed property", function() {
      return it("should return the longest name", function() {
        expect(scope.longestName()).to.be("Jimmies");
        scope.people.push("Jimmyjim");
        return expect(scope.longestName()).to.be("Jimmyjim");
      });
    });
    return describe("mocking a depdendency", function() {
      return it("should let us pass in whatever we want", function() {
        return expect(scope.version).to.equal("9.9.9!");
      });
    });
  });

}).call(this);

(function() {
  describe("app-version", function() {
    return it("should print current version", function() {});
  });

}).call(this);

(function() {
  describe("version service", function() {
    beforeEach(module("app"));
    return it("should return current version", inject(function(version) {
      return expect(version).to.equal("0.2.0");
    }));
  });

}).call(this);
