SELECT
	ut.USER_NAME USER_NAME
	,a.USER_ADDRESS USER_ADDRESS
from
	santas as s
inner JOIN
	users as ut
	on ut.user_id = s.target_id
inner JOIN
	users as us
	on us.user_id = s.santa_id
inner JOIN
	addresses as a
	on ut.user_id = a.user_id
WHERE
	us.USER_LOGIN = ?
;
