class LeaderBoardsController < ApplicationController
  def showAll
    @user = current_user
    @users = User.all
    @users = @users.sort { |a,b| b.score <=> a.score }
    @parent = Genre.distinct.pluck(:parent)
  end

  def showGenreWise
    @user = current_user
    @topic = params[:topic]
    @genre = Genre.where(parent: params[:topic])
    @touches = Array.new
    @genre.each do |t|
      @touches += Touch.where(genre_id: t.id)
    end
    @touch = @touches.group_by(&:user_id)
    @sum_by_user = []
    @touch.each do |id,values|
      @sum_by_user.push( {score: values.sum(&:score), user_id: User.find(id) } )
    end
    @sum_by_user.sort { |a,b| b[:score] <=> a[:score] }
    @parent = Genre.distinct.pluck(:parent)
  end

  def showTopicWise
    @user = current_user
    @touches  = Touch.where(genre_id: params[:id])
    @touches.sort { |a,b| b.score <=> a.score }
    @users = Array.new
    @touches.each do |t|
      @users.push(User.find(t.user_id))
    end
    @genre = Genre.find(params[:id])
    @genres = Genre.all
  end

end
