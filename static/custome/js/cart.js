const updateBtn =document.getElementsByClassName('update-cart')

for ( i =0;i < updateBtn.length ;i++){
 updateBtn[i].addEventListener('click',function(){
  const productId = this.dataset.product
  const action = this.dataset.action

  if(user ==='AnonymousUser'){
   addCookieItem(productId,action)
  }
  else{
   updateuserOrder(productId,action)
  }
 })
}


function addCookieItem(productId,action){
 if(action == 'add'){
  if(cart[productId] == undefined ){
   cart[productId]={'quantity':1}
  }else{
    cart[productId]=['quantity'] += 1
  }
 }
 if(action == 'remove'){
  cart[productId]=['quantity'] -= 1
  if(cart[productId]['quantity'] <= 0){
   delete cart[productId]
  }
 }
 location.reload()
}

function updateuserOrder(productId,action){
 fetch('update_item', {
  method:'POST',
  headers:{
   'Content-Type': 'application/json',
   'X-CSRFToken':csrftoken,
  },
  body:JSON.stringify({'productId':productId,'action':action})
 })
 .then((response)=>{
  return response.json()
 })
 .then((data)=>{
  location.reload();
 })
}
