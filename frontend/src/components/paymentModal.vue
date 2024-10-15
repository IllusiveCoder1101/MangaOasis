<template>
    <section class="modal">
        <div class="modal_container">
            
            <header class="modal_head">
                <h1 class="modal_header">Payment</h1>
                <button @click="close_func(true,true,true)" class="close_btn"><vue-feather type="x" class="icon3"/></button>
            </header>
            <form class="modal_form">
                <div class="card_details">
                    <div class="detail_container1">
                        <label for="card_name" class="modal_label">Name on Card</label>
                        <input type="text"  id="card_name" placeholder="John Doe" class="modal_input" required>
                    </div>
                    <div class="detail_container">
                        <label for="expiry" class="modal_label">Expiry</label>
                        <input type="text"  id="expiry" placeholder="mm-yyyy" class="modal_input" required>
                    </div>
                </div>
                <div class="card_details">
                    <div class="detail_container1">
                        <label for="card_no" class="modal_label">Card Number</label>
                        <input type="text"  id="card_no" placeholder="XXXX XXXX XXXX XXXX" class="modal_input" required>
                    </div>
                    <div class="detail_container">
                        <label for="cvv_no" class="modal_label">CVV</label>
                        <input type="password"  id="cvv_no" class="modal_input" placeholder="000" required>
                    </div>
                </div>
                <div class="payment_details">
                    <div class="detail_container2">
                        <p class="sub_text">Subtotal</p>
                        <p class="sub_text">${{ book_data[0]['book_price'] }}</p>
                    </div>
                    <div class="detail_container3">
                        <p class="sub_text1">Total</p>
                        <p class="sub_text1">${{ book_data[0]['book_price']}}</p>
                    </div>
                    <button type="submit" class="primary_btn1" @click.prevent="()=>{handle_submit(book_data[0]['book_price'])}">Place Your Order</button>
                </div>
            </form>
        </div>
    </section>
</template>

<script>
    export default{
        props:["close_func","book_data",'handle_submit']
    }
</script>