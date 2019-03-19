class OperationsController < ApplicationController
  def editDbs
    if is_admin?
      @user = current_user
      @genre = Genre.new
      @single_answer = SingleAnswer.new
      @allGenres = Genre.all
      @multiple_answer = MultipleAnswer.new
      @singleAnswers = SingleAnswer.all
      @multipleAnswers = MultipleAnswer.all
    else
      flash[:error] = "You are not an ADMIN"
      redirect_to root_url
    end
  end

  def addTopic
  end

  def delTopic
  end

  def addSubTopic
    @genre = Genre.new(params.require(:genre).permit(:parent, :subtype))
    if @genre.save
      flash[:success] = "subtopic created successfully"
      redirect_to editdbs_url
    else
      flash[:error] = "subtopic exists"
      redirect_to editdbs_url
    end
  end

  def delSubTopic
    @genre = Genre.find(params.require(:genre)[:id])
    Genre.destroy(@genre.id)
#    @touches = Touch.where(genre_id: @genre.id)
    flash[:success] = "subtopic deleted successfully"
    redirect_to editdbs_url
  end

  def addQuestion
    @single_answer = SingleAnswer.new(params.require(:single_answer).permit(:question, :option1, :option2, :option3, :option4, :answer, :genre_id, :url))
    if @single_answer.save
      flash[:success] = "Question added successfully"
      redirect_to editdbs_url
    else
      flash[:error] = "Question already exists"
      redirect_to editdbs_url
    end
  end

  def delQuestion
    @single_answer = Genre.find(params.require(:single_answer)[:id])
    SingleAnswer.destroy(@single_answer.id)
    flash[:success] = "question deleted successfully"
    redirect_to editdbs_url
  end

  def addMultipleQuestion
    @multiple_answer = MultipleAnswer.new(params.require(:multiple_answer).permit(:question, :option1, :option2, :option3, :option4, :answer1, :answer2, :answer3, :answer4, :genre_id, :url))
    if @multiple_answer.save
      flash[:success] = "Question added successfully"
      redirect_to editdbs_url
    else
      flash[:error] = "Question already exists"
      redirect_to editdbs_url
    end
  end

  def delMultipleQuestion
    @multiple_answer = MultipleAnswer.find(params.require(:multiple_answer)[:id])
    MultipleAnswer.destroy(@multiple_answer.id)
    flash[:success] = "question deleted successfully"
    redirect_to editdbs_url
  end

end
