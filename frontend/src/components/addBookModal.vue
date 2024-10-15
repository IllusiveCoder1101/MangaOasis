<template>
    <section class="modal">
        <div class="modal_container">
            
            <header class="modal_head">
                <h1 class="modal_header">Add Book</h1>
                <button @click="close_func()" class="close_btn"><vue-feather type="x" class="icon3"/></button>
            </header>
            <form class="modal_form">
                <div class="card_details">
                    <div class="detail_container1">
                        <label for="card_name" class="modal_label">Book Name</label>
                        <input type="text"  id="card_name" placeholder="XYZ" class="modal_input" required v-model="book_data['book_name']">
                    </div>
                    <div class="detail_container">
                        <label for="expiry" class="modal_label">Author</label>
                        <input type="text"  id="expiry" placeholder="ABC" class="modal_input" required v-model="book_data['author_name']">
                    </div>
                    
                </div>
                <div class="card_details">
                    <div class="detail_container5">
                        <label for="expiry" class="modal_label">Book Genres</label>
                        <input type="text"  id="expiry" placeholder="ABC,XYZ" class="modal_input" required v-model="book_data['book_genres']">
                    </div>
                    
                </div>
                <div class="card_details">
                    <div class="detail_container5">
                        <label for="expiry" class="modal_label">Book Description</label>
                        <textarea  id="comment" cols="60" rows="7" class="modal_input" placeholder="Write the description" required v-model="book_data['book_description']"></textarea>
                    </div>
                    
                </div>
                <div class="card_details">
                    <div class="detail_container1">
                        <label for="expiry" class="modal_label">Book Cover</label>
                        <input type="file" name="" id="" ref="file" class="modal_input" required @change="book_data['book_cover']=read_img()">
                    </div>
                    <div class="detail_container">
                        <label for="expiry" class="modal_label">Price</label>
                        <input type="number"  id="expiry" placeholder="10" class="modal_input" required v-model="book_data['book_price']">
                    </div>
                </div>
                <div v-if="error.length>0" class="error_state3">
                    <p class="error_msg">{{ error }}</p>
                </div>
                <div class="payment_details">
                    <button type="submit" class="primary_btn1" :disabled="checkData()"   @click.prevent="()=>{handle_add_book(book_data)}">Add Book</button>
                </div>
            </form>
        </div>
    </section>
</template>

<script setup>
    import { ref } from 'vue';
    const book_data=ref({"book_name":"","author_name":"","book_genres":"","book_description":"","book_cover":"","book_price":""})
    const checkData=()=>{
                
        if (book_data.value['book_name'] && book_data.value["author_name"] && book_data.value["book_genres"] && book_data.value["book_description"] && book_data.value["book_cover"] && book_data.value["book_price"] ) {
           
            return false
        }
        else{
            
            return true
        }
    }

    
</script>

<script>
    export default {
        props:["close_func","handle_add_book","error"],
        
        methods:{
            read_img(){
                return this.$refs.file.files[0].name
            }
        }
    }
</script>