//gist.github.com/x-yuri/c229b3f9e8282ea12cecbbe923cc61c1

https: db.getSiblingDB("admin").auth(
  process.env.MONGO_INITDB_ROOT_USERNAME,
  process.env.MONGO_INITDB_ROOT_PASSWORD
);
db.createUser({
  user: process.env.MONGO_USER,
  pwd: process.env.MONGO_PASSWORD,
  roles: ["readWrite"],
});
