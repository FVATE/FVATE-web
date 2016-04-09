(function() {
  var app, config, express, fs;

  express = require('express');

  fs = require('fs');

  config = require('./config');

  app = express();

  app.set('info', {
    name: config.appinfo
  });

  app.configure('local', function() {
    return app.use(express["static"]('app'));
  });

  app.configure('develop', function() {
    return app.use(express["static"]('app'));
  });

  app.configure('prod', function() {
    return app.use(express["static"]('build'));
  });

  app.use(express.bodyParser());

  app.use(require('./middleware/logging')());

  fs.readdirSync(__dirname + '/routes').forEach(function(file) {
    return require('./routes/' + file)(app);
  });

  app.listen(config.port);

}).call(this);

(function() {
  module.exports = {
    port: 3000,
    appinfo: {
      name: "Open Web App"
    }
  };

}).call(this);

(function() {
  module.exports = function() {
    return function(req, res, next) {
      if (req.url === "/") {
        console.log('nodeapp', 'middleware');
      }
      return next();
    };
  };

}).call(this);

(function() {
  module.exports = function(app) {
    return app.get('/about', function(req, res) {
      return res.end('<h1>About ' + app.get('info').name(+'</h1>'));
    });
  };

}).call(this);

/*
/**
  * Example web services.
  * One would normally communicate with a database to get the data.
  *
*/


(function() {
  module.exports = function(app) {
    var getUser, users;
    users = [
      {
        name: 'Frodo',
        id: 1
      }, {
        name: 'Samwise',
        id: 2
      }, {
        name: 'Merry',
        id: 3
      }, {
        name: 'Pippin',
        id: 4
      }
    ];
    app.get('/user', function(req, res) {
      return res.send(users);
    });
    app.get('/user/:id', function(req, res) {
      var id, user;
      id = parseInt(req.params.id, 10);
      user = getUser(id);
      return res.send(user);
    });
    app.put('/user/:id', function(req, res) {
      var user;
      user = req.body;
      user.awesome = true;
      users[user.id - 1] = user;
      return res.send(user);
    });
    app.post('/user', function(req, res) {
      var user;
      user = req.body;
      user.id = users.length;
      user.cool = true;
      users.push(user);
      res.set("content-location", "/users/" + user.id);
      return res.send(201, user);
    });
    app.del('/user/:id', function(req, res) {
      var id, user;
      id = parseInt(req.params.id, 10);
      user = getUser(id);
      if (user) {
        users.splice(user.id - 1, 1);
      }
      return res.send(204);
    });
    /*
    /*
     * get user by id
     * real service would interact with a real data source
     * @param  {String} id
     * @return {Object} user
     *
    */

    return getUser = function(id) {
      return users.filter(function(user) {
        return user.id === id;
      })[0];
    };
  };

}).call(this);
