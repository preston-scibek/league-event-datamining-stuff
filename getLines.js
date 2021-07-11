// https://frontpage.na.leagueoflegends.com/en_US/channel/lol/home/event/sentinels-hub-2021#/

x = document.getElementsByTagName('script');

items = [];
x.forEach((item, i) => {
	if (item.type == "text/i18n"){
		temp = [];
		temp.push(item.text)
		temp.push(item.id)
		items.push(temp);
	}
})

var str = JSON.stringify(items, null, 2);
console.log(str)