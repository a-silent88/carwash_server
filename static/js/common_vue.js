// window.getFrom = new Vue({
//     delimiters: ['[[', ']]'],
//     // el: '#result',
//     data() {
//         return {
//         info: [],
//         htmlData: []
//         };
//     },
//     methods: {
//         putItem(pk, name, value){
//             req = {
//                 [name] : value
//             }
//             const auth = {
//                 headers: {Authorization:'Token 7f5ee56bdc726573e361a3251dd5d92972eb93e0'} 
//             }

//             axios
//             .put('/api/orderspay/' + pk + '/', req, auth)
//             .then(response => {})
//             .catch(function(error){
//                 console.log(error);
//             });
//         },
//         getItem(url, item, pk, elem){
//             headers = {
//                 headers: {
//                     'Content-Type': 'application/html'
//                 }           
//             }
//             axios
//             .get(url, headers)
//             .then(response => (this.htmlData = response.data))
//         }
//     },
//     mounted() {
//         this.getItem(this.$el.dataset.url);
//     }
//     });
// // getFrom.$mount('#result');