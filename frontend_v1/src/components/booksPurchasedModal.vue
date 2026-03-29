<template>
    <section class="modal">
        <div class="modal_container">
            
            <header class="modal_head">
                <h1 class="modal_header">Purchased</h1>
                <button @click="close_func(0)" class="close_btn"><vue-feather type="x" class="icon3"/></button>
            </header>
            <div class="issue_book_container">
                <div v-if="user_books_purchased.length>0">
                    <div class="issue_profile1" v-for="i in user_books_purchased" :key="i">
                        <div class="issue_desc">
                            <img :src="getBookCover(i['book_id'])" alt="profile_pic" class="profile_pic">
                            <div class="user_card_desc">
                                <p class="user_card_name1">{{ getBookById(i["book_id"])[0]["book_name"] }}</p>
                                <p class="user_card_email1">{{ getBookById(i["book_id"])[0]["author_name"] }}</p>
                            </div>
                        </div>
                        <p class="issued_expiry1"> ${{ getBookById(i["book_id"])[0]["book_price"] }} </p>
                    </div>
                </div>
                <div v-else class="error_state1">
                    <p class="error_msg1">No Books Purchased</p>
                </div>
            </div>
            
        </div>
    </section>
</template>


<script>
    export default {
        props:["close_func","user_books_purchased","getBookById","getBookCover"]
    }
</script>