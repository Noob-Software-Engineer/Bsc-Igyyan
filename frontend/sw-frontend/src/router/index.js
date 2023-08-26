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
    // route level code-splitting
    // this generates a separate chunk (About.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: Login
  },
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
