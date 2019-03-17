class UsersController < ApplicationController
  def show
    @user = User.find(params[:id])
    @touch = Touch.where(user_id: @user[:id])
    @genres = []
    @touch.each do |t|
      @genres.push(Genre.find(t[:genre_id]))
    end
  end
  def new
    @user = User.new
  end
  def create
    @user = User.new(params.require(:user).permit(:name, :email, :password, :password_confirmation))
    @user.score = 0
    if @user.save
      log_in @user
      flash[:success] = "Welcome to the Sample App!"
      redirect_to @user
    else
      render 'new'
    end
  end
end
