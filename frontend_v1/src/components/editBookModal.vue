<template>
    <section class="modal">
        <div class="modal_container">
            
            <header class="modal_head">
                <h1 class="modal_header">Edit Book</h1>
                <button @click="close_func()" class="close_btn"><vue-feather type="x" class="icon3"/></button>
            </header>
            <form class="modal_form">
                <div class="card_details">
                    <div class="detail_container1">
                        <label for="card_name" class="modal_label">Book Name</label>
                        <input type="text"  id="card_name" placeholder="XYZ" class="modal_input" :value="get_book['book_name']" @input="book_data['book_name']=$event.target.value">
                    </div>
                    <div class="detail_container">
                        <label for="expiry" class="modal_label">Author</label>
                        <input type="text"  id="expiry" placeholder="ABC" class="modal_input" :value="get_book['author_name']" @input="book_data['author_name']=$event.target.value">
                    </div>
                    
                </div>
                <div class="card_details">
                    <div class="detail_container5">
                        <label for="expiry" class="modal_label">Book Genres</label>
                        <input type="text"  id="expiry" placeholder="ABC,XYZ" class="modal_input" :value="get_book['book_genres']" @input="book_data['book_genres']=$event.target.value">
                    </div>
                    
                </div>
                <div class="card_details">
                    <div class="detail_container5">
                        <label for="expiry" class="modal_label">Book Description</label>
                        <textarea  id="comment" cols="60" rows="7" class="modal_input" placeholder="Write the description" :value="get_book['book_description']" @input="book_data['book_description']=$event.target.value"></textarea>
                    </div>
                    
                </div>
                <div class="card_details">
                    <div class="detail_container1">
                        <label for="expiry" class="modal_label">Book Cover</label>
                        <input type="file" name="" id="" ref="file"  class="modal_input" @change="book_data['book_cover']=read_img()">
                    </div>
                    <div class="detail_container">
                        <label for="expiry" class="modal_label" >Price</label>
                        <input type="number"  id="expiry" placeholder="10" class="modal_input" :value="get_book['book_price']" @input="book_data['book_price']=$event.target.value">
                    </div>
                </div>
                <div v-if="error.length>0" class="error_state3">
                    <p class="error_msg">{{ error }}</p>
                </div>
                <div class="payment_details">
                    
                    <button type="submit" class="primary_btn1" @click.prevent="edit_book(book_data,get_book['book_id'])">Edit Book</button>
                </div>
            </form>
        </div>
    </section>
</template>


<script setup>
    import { ref } from 'vue';
    const book_data=ref({"book_name":"","author_name":"","book_genres":"","book_description":"","book_cover":"","book_price":""})
    

    
</script>

<script>
    export default {
        props:["close_func","get_book","edit_book","error"],
        
        methods:{
            read_img(){
                return this.$refs.file.files[0].name
            }
        }
    }
</script>