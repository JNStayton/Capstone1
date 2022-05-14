// async function example(evt) {
// 	evt.preventDefault();

// 	resp = await axios.post('/api/get-all-games');
// 	console.log(resp.data);
// }

// $('#example').on('submit', example);

// showTop10Games();

// function makeGameDisplay(game) {
// 	return `
//         <div class="card m-1 col-md-3">
//         style="position: absolute; top: 0; right: 0"
//             <img src="${game.image_url}" class="card-img-top" style="height: 15rem; object-fit: cover;"alt="A picture of a ${game.name}">
//             <div data-id="${game.id}" class="card-body">
//                 <h5 class="card-title">${game.name.toUpperCase()} <span class="badge badge-success">$${game.price}</span></h5>
//                 <span class="badge badge-warning">${game.min_players}-${game.max_players} Players</span>
//                 <span class="badge badge-dark">${game.min_playtime}-${game.max_playtime} Minutes</span>
// 				<a href="/games/${game.id}" class="btn btn-info m-2 view">View Game</a>
//             </div>
//         </div>
// `;
// }

// async function showTop10Games() {
// 	resp = await axios.get('/api/get-all-games');
// 	games = resp.data;
// 	for (let game of games) {
// 		$('#container').append(makeGameDisplay(game));
// 	}
// }
