class ScoreBoardController < ApplicationController
  def show
    @user = current_user
    
    @touch = []
    @genre = Genre.all
    @genre.each do |t|
      
  end
end
