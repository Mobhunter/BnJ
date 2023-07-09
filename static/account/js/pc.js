document.addEventListener("DOMContentLoaded", get_user);
function get_user(event){

	let user_data = new  XMLHttpRequest();
	let posts_data = new  XMLHttpRequest();
	user_data.open("GET","");
	posts_data.open("GET","")
	user_data.responseType="json";
	posts_data.responseType="json";
	user_data.send();
	posts_data.send()
	user_data.onload=function(event){
		user=user_data.response;
		for (i in user){
		if(i=="name"){
			let name=document.body.querySelector(".user-name");
			name.innerHTML=user[i];
		}
		else if(i=="img"){
			let img=document.body.querySelector(".user-photo");
			img.src=user[i];
		}
		else if(i=="genre"){
			let sidebar=document.getElementById("genre-list");
			if(user[i].length>=1){
				for(let j of user[i]){
					sidebar.innerHTML+=j+" ";
				}
			}
			else{
				sidebar.innerHTML="не указан"
			}
		}
	}
	posts_data.onload()=function(){
		user_posts=posts_data.response;
		let posts_amount_in_storage=user_posts.length;
		if ((posts_amount_in_storage<5) && (posts_amount_in_storage>0)){
			for (let postworked in user_posts){
				let post_element=document.createElement("article");
				let appended_element=document.querySelector(".main-info-adder");
				let appendants= new Map();
				let MRO=["message_part","audio_part","date_part"];
				let MROindex=0;
				let MROlen=0;
				for(let j in user_posts[postworked]){
					if(j=="message"){
						if(user_posts[postworked][j]!=undefined){
							let message_part=document.createElement("section");
							message_part.classList.add("message_part");
							message_part.textContent=user_posts[postworked][j];
							appendants.set("message_part",message_part);
							MROlen++;
						}
						else{
							appendants.set("message_part",undefined);
							MROlen++;
						}
					}
					else if(j=="date"){
						let date_part=document.createElement("span");
						date_part.classList.add("date_part");
						date_part.textContent=user_posts[postworked][j];
						appendants.set("date_part",date_part);
						MROlen++;
					}
					else if(j=="audio"){
						if(user[i][postworked][j]!=undefined){
							let audio_part=document.createElement("audio");
							audio_part.classList.add("audio_part");
							audio_part.src=user_posts[postworked][j];
							audio_part.controls=true;
							appendants.set("audio_part",audio_part);
							MROlen++;
						}
						else{
							appendants.set("audio_part",undefined);
							MROlen++;
						}
					}
				}
				let post_element_len=0;
				while(MROindex<3){
					let elem=appendants.get(MRO[MROindex])
					if(elem!=undefined){post_element.append(elem);post_element_len++}
					MROindex++;
				}
				if(post_element_len>1)
				{
					appended_element.prepend(post_element);
				}
			}
		}
	}
}

	}	
	/*let user={
		name:"Вадим Клинк",
		img:"C:/Users/chepr/Desktop/Проекты/проект BoJ/шаблоны/photoes/example_photo.jpg",
		genre:["Хэви-металл","Трэш-металл","Блюз-рок","Фолк-рок",],
		instruments:["Ударная установка","Ритм-гитара","Бэк-вокал"],
		favourite_bands:["Metallica","Megadeth","Led Zeppelin"],
		songs:[
			"Motörhead-Till The End",
			"Ari Hest-After the Thunder",
			"Linkin Park-One More Light",
			"Metallica-One",
			"Eminem feat. Dido-Stan",
			"Black Sabbath-Changes",
			"Guns N Roses-Patience",
			"Five Finger Death Punch-I Refuse",
			"Megadeth-A Tout Le Monde",
			"Noize MC-Жвачка Video Edit",
			"Metallica-The Day That Never Comes",
			"Journey-Separate Ways",
			"Metallica-The Unforgiven II",
			"Scorpions-Humanity",
			"Jubilee-Кладбище имени меня",
			"Linkin Park-What I ve Done",
			"Linkin Park-In the End",
			"Linkin Park-Numb",
			"Aerosmith-Dream On",
			"Johny Cash-Hurt",
			"Bob Dylan-Knockin On Heaven Door",
			"Guns N Roses-Dont Cry",
			"Limp Bizkit-Behind Blue Eyes",
			"The Beatles-Yesterday",
			"Megadeth-Tears In a Vial",
		],
		posts:{
			length:2,
			post1:{
				date:"11.02.2002",
				//message:undefined,
				//message:"Metallica (читается как Мета́ллика) — американская метал-группа[1], образованная в 1981 году, в Лос-Анджелесе. Metallica оказала большое влияние на развитие метала и входит (вместе с такими группами как Slayer, Megadeth и Anthrax) в «большую четвёрку трэш-метала»[2]. Альбомы Metallica были проданы в общей сложности в количестве более 110 миллионов экземпляров по всему миру[3], что делает её одним из самых коммерчески успешных металлических коллективов. В 2011 году один из крупнейших журналов о метал-музыке Kerrang! в июньском номере признал Metallica лучшей метал-группой последних 30 лет[4].Группа получила сторонников в среде поклонников андеграундной музыки и одобрительные отзывы критиков, выпустив третий студийный альбом Master of Puppets (1986), который сейчас считается «классикой трэш-метала» и который существенно повлиял на дальнейшее развитие этого жанра. Коммерческий успех пришёл после выпуска пятого альбома The Black Album или «Metallica», который дебютировал на первой строчке чарта Billboard 200. В 2000 году Metallica были в числе музыкальных исполнителей, подавших иск против Napster, в связи с бесплатным распространением материалов, защищённых авторским правом, без разрешения авторов. В результате, была достигнута договорённость, по которой Napster стал платным сервисом. Несмотря на первое место в Billboard 200, альбом St. Anger (2003) из-за отсутствия гитарных соло, «стального звучания» малого барабана и сырости звучания разочаровал многих фанатов группы. В фильме Some Kind of Monster показан процесс создания St. Anger и отношения между участниками группы в течение этого времени. В 2009 году Metallica была введена в Зал славы рок-н-ролла. В 2012 году Metallica основали независимый лейбл Blackened Recordings и выкупили права на все свои студийные альбомы и видео. В 2019 году группа вошла в список самых высокооплачиваемых музыкантов по версии журнала Forbes. Заработанная сумма составила $68,5 млн, это десятое место в рейтинге[5].",
				audio:"C:/Users/chepr/Desktop/Музыка/Metallica - Fuel.mp3",
			},
			post2:{
				date:"12.02.2002",
				message:"Metallica была основана в Лос-Анджелесе 28 октября 1981 года[6] гитаристом и вокалистом Джеймсом Хэтфилдом и барабанщиком Ларсом Ульрихом после того, как оба поместили объявление о создании группы в издании «The Recycler». Однако, как позже выяснилось из интервью Рона Макговни журналу «So What!», Джеймса и Ларса познакомил между собой их общий друг Хью Таннер, который в то время был соло-гитаристом в группе Рона и Джеймса «Leather Charm». Дуэт пригласил басиста Рона Макговни, знакомого Хэтфилда по его предыдущей группе «Leather Charm», однако на ранних стадиях существования группы постоянно возникали проблемы с гитаристами, поэтому уже поначалу их сменилось несколько: Ллойд Грант, Брэд Паркер и Джефф Уорнер. Metallica получила своё название, когда Рон Куинтана попросил Ларса Ульриха помочь ему выбрать название для своего нового журнала об американских и британских метал-группах. Куинтана имел такие варианты как «Metallica», «Metal Mania» и «Hesse». Ульрих сообразил, что «Metallica» будет отличным названием группы и сказал Рону, что такое название вряд ли кому-нибудь понравится.",
				audio:"C:/Users/chepr/Desktop/Музыка/Metallica - Fuel.mp3",
			}
		}
	}*/