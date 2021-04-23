//Получение объекта пользователя
/*let user={
	link:"https://www.youtube.com/watch?v=dQw4w9WgXcQ",
	name:"Вадим Клинк",
	icon:"css/photoes/example_photo.jpg",
	chats:[{
		name:"Хэтфилд",
		icon:"css/photoes/hatfield.jpg",
		last_message:"fuck it all and no regrets",
		lm_date:"8:30",
		link:"chat.html",
		date:"2012-11-01T16:30:10"
	},{
		name:"Мастейн",
		icon:"css/photoes/Mastein.jpg",
		last_message:"it\'s stil we, the people right?",
		link:"chat.html",
		lm_date:"15:35",
		date:"2013-11-01T16:30:10"
	},{
		name:"Гизер",
		icon:"css/photoes/Gizer.jpg",
		link:"chat.html",
		lm_date:"9:24",
		date:"2013-11-01T16:30:12"
	},{
		name:"Тони",
		icon:"css/photoes/Iommi.jpg",
		last_message:"I am ironman",
		link:"chat.html",
		lm_date:"10:15",
		date:"2010-11-01T16:30:10"
	},{
		name:"Хэнсли",
		icon:"css/photoes/Hensli.jpg",
		last_message:"",
		link:"chat.html",
		lm_date:"9:06",
		date:"2013-10-02T16:30:10"
	},{
		name:"Хэтфилд",
		icon:"css/photoes/hatfield.jpg",
		last_message:"fuck it all and no regrets",
		lm_date:"8:30",
		link:"chat.html",
		date:"2012-11-01T16:30:10"
	},{
		name:"Мастейн",
		icon:"css/photoes/Mastein.jpg",
		last_message:"it\'s stil we, the people right?",
		link:"chat.html",
		lm_date:"15:35",
		date:"2013-11-01T16:30:10"
	},{
		name:"Гизер",
		icon:"css/photoes/Gizer.jpg",
		link:"chat.html",
		lm_date:"9:24",
		date:"2013-11-01T16:30:12"
	},{
		name:"Тони",
		icon:"css/photoes/Iommi.jpg",
		last_message:"I am ironman",
		link:"chat.html",
		lm_date:"10:15",
		date:"2010-11-01T16:30:10"
	},{
		name:"Хэнсли",
		icon:"css/photoes/Hensli.jpg",
		last_message:"",
		link:"chat.html",
		lm_date:"9:06",
		date:"2013-10-02T16:30:10"
	}]
}*/

//В дальнейшем получить рексестом
let api_url = new URL(window.location.origin + "/api/messaging/get_chats");
$.ajax({ 
	url: api_url.href, 
    dataType: "json", // Для использования JSON формата получаемых данных
	method: "GET", // Что бы воспользоваться POST методом, меняем данную строку на POST   		  
	}).done(function(data) {
		get_chats(data);
	});


let chat_list=[];
//Подключение сборщика
//функция сортировки 
function sort_arr(a,b){
	a=Date.parse(a["date"]);
	b=Date.parse(b["date"]);
	if(a>b){return 1}
	else if(a==b){return 0}
	else {return -1};
}
//функция сборки
function get_chats(data){
	let user = data;
	user["chats"].sort(sort_arr);
	let info_adder=document.querySelector(".chats");
	outer:for (let i of user["chats"]){
		let item=document.createElement("article");

		let name=document.createElement("span");

		let icon=document.createElement("img");

		let last_message=document.createElement("span");
		let lm_date=document.createElement("span");

		let option=document.createElement("div");
		let button=document.createElement("button");
		button.innerHTML="&#8942;";
		option.append(button);

		let needed_data=new Set(["name","icon","last_message","link"]);
		let appendants=new Map();
		let MRO=["icon","name","last_message","lm_date","options"];

		inner:for (let j in i){
			switch(j){
				case "name":{
					if(i[j]!=undefined || i[j]!=null){
						name.textContent=i[j];
						needed_data.delete(j);
						appendants.set("name",name);
					}
					break;
				}
				case "icon":{
					if(i[j]!=undefined || i[j]!=null){
						icon.src=i[j];
						needed_data.delete(j);
						appendants.set("icon",icon);
					}
					break;
				}
				case "last_message":{
					if(i[j]!=undefined || i[j]!=null){
						last_message.textContent=i[j];
						needed_data.delete(j);
						appendants.set("last_message",last_message);
					}
					break;
				}
				case "link":{
					if(i[j]!=undefined || i[j]!=null){
						item.setAttribute("link",i[j]);
						needed_data.delete(j);
					}
					break;
				}
				case "lm_date":{
					if(i[j]!=undefined || i[j]!=null){
						lm_date.textContent=i[j];
						needed_data.delete(j);
						appendants.set("lm_date",lm_date);
					}
					break;
				}
			}
		}
		if (needed_data.size!=0){
			for (let j of needed_data){ 
				switch(j){
					case "icon":{
						icon.src="css/photoes/no.jpg";
						needed_data.delete(j);
						appendants.set("icon",icon);
						break;
					}
					case "last_message":{
						delete last_message;
						needed_data.delete(j);
						break;
					}
					case "link":{
						continue outer;
					}
					case "lm_date":{
						delete lm_date;
						needed_data.delete(j);
						break;
					}
				}
			}
		}
		let ul=document.createElement("ul");
		for(let key of MRO){
			if(appendants.has(key)){
				let li=document.createElement("li");
				li.append(appendants.get(key));
				li.classList.add(key);
				ul.append(li)
			}
			continue;
		};
		item.append(ul);
		info_adder.append(item);
		chat_list.push(item);
		info_adder.addEventListener("click",open_chat);
	}
	let needed_data=new Set(["name", "icon"])
	outer2:for(let i in user){
		if(i=="name"){
			let name=document.body.querySelector(".user-name");
			name.textContent=user[i];
			needed_data.delete(i);

		}
		else if(i= "icon"){
			let icon=document.body.querySelector(".user-photo");
			icon.src=user[i];
			needed_data.delete(i);
		}
	}
	outer3:for(let i of needed_data){
		switch(i){
			case "name":{
				if(!("name" in user))user["name"]="Не указано";
				let name=document.body.querySelector(".user-name");
				name.textContent="Не указано";
				break;
			}
			case "icon":{
				if(!("icon" in user))user["icon"]="css/photoes/no.jpg";
				let icon=document.body.querySelector(".user-photo");
				icon.src="css/photoes/no.jpg";
				break;
			}	
		}
	}
}
//Подключение сборщика
function open_chat(event){
	let article=this.querySelector("article");
	let link=article.hasAttribute("link");
	if(link){
		let inputer=document.getElementsByName("search_bar")[0];
		inputer.value="";
		document.location.href = article.getAttribute("link");
	}
}
//поиск бесед
document.getElementsByName("search_bar")[0].addEventListener("input",search)
function search(event){
	let info_adder=document.querySelector(".chats");
	info_adder.innerHTML=null;
	if(this.value==""){
		for(let i of chat_list){
			info_adder.append(i);
		}
	}
	else{
		let value=this.value;
		for(let i of chat_list){
			let name=i.querySelector(".name span")
			if(name.textContent.toLowerCase().includes(value.toLowerCase()))info_adder.append(i);
		}
		if(info_adder.innerHTML==""){
			let i=document.createElement("span");
			i.textContent="Пользователь не найден";
			i.classList.add("no_user");
			info_adder.append(i);
		}
	}
}