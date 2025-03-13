ECS="http://iacobu-publi-0jdai9cq4e6h-802951250.eu-central-1.elb.amazonaws.com"
LAMBDA="https://s2myg4pgdsxgj4wbjggdp7l2fy0kssda.lambda-url.eu-central-1.on.aws"

URL="/users/whoLikedPostsByAuthors"

RAW="Raw"
ACTIVERECORD="ActiveRecord"
QUERYBUILDER="QueryBuilder"

PARAMETERS='?authors=user-1,user-2,user-3,user-4,user-5,user-6,user-7,user-8,user-9,user-10'

function test {
	echo "$1"
	hey "$1"
	echo
	echo
}

(
test "$ECS$URL$QUERYBUILDER$PARAMETERS"
test "$ECS$URL$ACTIVERECORD$PARAMETERS"

test "$LAMBDA$URL$QUERYBUILDER$PARAMETERS"
sleep 15
test "$LAMBDA$URL$ACTIVERECORD$PARAMETERS"
) > testing/results.txt