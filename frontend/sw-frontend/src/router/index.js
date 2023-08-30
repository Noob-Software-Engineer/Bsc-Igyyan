import { createRouter, createWebHistory } from 'vue-router'
import Register from '../views/Register.vue'
import Login from '../views/Login.vue'
import Test from '../views/Test.vue'
import Post from '../views/Post.vue'
import Social from '../views/Social.vue'
import PostDetails from '../views/PostDetails.vue'
import TestDetails from '../views/TestDetails.vue'


const routes  = [
  {
    path: '/register',
    name: 'register',
    component: Register 
  },
  {
    path: '/login',
    name: 'login',
    component: Login
  },
  // {
  //   path: '/user/:id',
  //   name: 'User Details',
  //   component: UserDetails,
  //   props: true,
  // },
  {
    path: '/posts',
    name: 'Post',
    component: Post
  },
  {
    path: '/posts/:id',
    name: 'Post Details',
    component: PostDetails,
    props: true
  },
  {
    path: '/tests',
    name: 'Test',
    component: Test
  },
  {
    path: '/test/:id',
    name: 'Test Details',
    component: TestDetails,
    props: true
  },
  {
    path: '/social',
    name: 'Social',
    component: Social,
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes 
})

export default router
