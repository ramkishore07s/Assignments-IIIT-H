Rails.application.routes.draw do
  
  get '/scoreboard', to: 'score_board#show'
  
  post '/retake', to: 'quizzes#retake'
  
  resources :users  
  get '/scores', to: 'leader_boards#showAll'

  get '/genre/:topic', to: 'leader_boards#showGenreWise'

  get '/scores/:id', to: 'leader_boards#showTopicWise'

  get '/genres', to: 'quizzes#showGenres'

  get '/genres/:genre', to: 'quizzes#showTopics'

  get '/:genre/:topic', to: 'quizzes#showQuestions'

  post '/updateScore', to: 'quizzes#updateScore'

  post '/updateMultipleScore', to: 'quizzes#updateMultipleScore'
  
  get '/editdbs', to: 'operations#editDbs'

  post '/addTopic', to: 'operations#addTopic'

  post '/delTopic', to: 'operations#delTopic'

  post '/addSubTopic', to: 'operations#addSubTopic'

  post '/delSubTopic', to: 'operations#delSubTopic'

  post '/addQuestion', to:  'operations#addQuestion'

  post '/delQuestion', to: 'operations#delQuestion'

  post '/addMultipleQuestion', to: 'operations#addMultipleQuestion'

  post '/delMultipleQuestion', to: 'operations#delMultipleQuestion'

  get 'sessions/new'
  
  root 'static_pages#home'
  get '/home', to: 'static_pages#home'
  get '/about', to: 'static_pages#about'
  get '/help', to: 'static_pages#help'
  get '/signup', to: 'users#new'
  post '/signup', to: 'users#create'
  get    '/login',   to: 'sessions#new'
  post   '/login',   to: 'sessions#create'
  delete '/logout',  to: 'sessions#destroy'
  post '/google', to: 'sessions#google'
  # For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html
end
