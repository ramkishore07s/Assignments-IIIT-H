class QuizzesController < ApplicationController
  def showGenres
    @user = current_user
    @genres = Genre.distinct.pluck(:parent)
  end
  
  def showTopics
    @user = current_user
    @genre = Genre.distinct.pluck(:parent)
    @genres = Genre.where(parent: params[:genre])
    @head = params[:genre]
  end

  def showQuestions
    @user = current_user
    @touch = Touch.new
    @single_choices = SingleChoice.new
    @genre = Genre.find_by(parent: params[:genre], subtype: params[:topic])
    @single_answers = SingleAnswer.where(genre_id: @genre.id).all
    @touches = Touch.find_by(genre_id: @genre.id,user_id: current_user.id)
    
    if !@touches
      @touches = Touch.new(genre_id: @genre.id,user_id: current_user.id,score:0)
      @touches.save
    end
    @topics = Genre.where(parent: @genre.parent)

    @multiple_choices = MultipleChoice.new
    @multiple_answers = MultipleAnswer.where(genre_id: @genre.id).all

    @marked_single = []
    @single_answers.each do |t|
      a = SingleChoice.where(touch_id: @touches[:id],single_answer_id: t[:id])
      if a.length > 0
        if a[0][:answer] == t[:answer]
          @marked_single.push("c")
        else
          @marked_single.push("i")
        end
      else
        @marked_single.push("u")
      end
    end

    @marked_multiple = []
    @multiple_answers.each do |t|
      b = MultipleChoice.where(touch_id: @touches[:id], multiple_answer_id: t[:id])
      if b.length > 0
        if check2(b,t)
          @marked_multiple.push("c")
        else
          @marked_multiple.push("i")
        end
      else
        @marked_multiple.push("u")
      end
    end
  end

  def updateScore
    @posted = params.require(:single_choice)
    @question = SingleAnswer.find(@posted[:single_answer_id])
    
    @single_choices = SingleChoice.find_by(@posted.permit(:touch_id,:single_answer_id))

    if !!@single_choices
      if @question[:answer] != @posted[:answer]
        if @single_choices.answer == @question[:answer]
          decrement(@posted[:touch_id])
        end
      else 
        if @single_choices.answer != @posted[:answer]
          increment(@posted[:touch_id])
        end
      end
      @single_choices.answer = @posted[:answer]
      @single_choices.save
        
    else
      @single_choices = SingleChoice.new(@posted.permit(:touch_id, :single_answer_id, :answer))
      if @question[:answer] == @posted[:answer]
        increment(@posted[:touch_id])
      end
      @single_choices.save
    end
    @temp = Genre.find(Touch.find(@single_choices[:touch_id])[:genre_id])
    return redirect_to ("/"  +  @temp[:parent] + "/" + @temp[:subtype] )
  end

  def updateMultipleScore
    @posted = params.require(:multiple_choice)
    @question = MultipleAnswer.find(@posted[:multiple_answer_id])
    
    @multiple_choices = MultipleChoice.where(@posted.permit(:touch_id,:multiple_answer_id))
    
    if @multiple_choices.length > 0
      if !check(@question,@posted)
        if check2(@multiple_choices,@question)
          decrement(@posted[:touch_id])
        end
      else
        if !check2(@multiple_choices, @posted)
          increment(@posted[:touch_id])
        end
      end
      @multiple_choices[0][:answer1] = @posted[:answer1]
      @multiple_choices[0][:answer2] = @posted[:answer2]
      @multiple_choices[0][:answer3] = @posted[:answer3]
      @multiple_choices[0][:answer4] = @posted[:answer4]
      
      @multiple_choices[0].save
        
    else
      @multiple_choices = []
      @multiple_choices.push(MultipleChoice.new(@posted.permit(:touch_id, :multiple_answer_id, :answer1,:answer2, :answer3,:answer4)))
      if check(@question, @posted)
        increment(@posted[:touch_id])
      end
      @multiple_choices[0].save
    end
    @temp = Genre.find(Touch.find(@multiple_choices[0][:touch_id])[:genre_id])
    return redirect_to ("/"  +  @temp[:parent] + "/" + @temp[:subtype] )
  end

  def check(question, posted)
    ( a(@question[:answer1]) == a(@posted[:answer1]) ) && ( a(@question[:answer2]) == a(@posted[:answer2])) && ( a(@question[:answer3]) == a(@posted[:answer3]) ) && ( a(@question[:answer4]) == a(@posted[:answer4]))
  end

  
  def check2(question, posted)
    ( a(question[0][:answer1]) == a(posted[:answer1]) ) && ( a(question[0][:answer2]) == a(posted[:answer2])) && ( a(question[0][:answer3]) == a(posted[:answer3]) ) && ( a(question[0][:answer4]) == a(posted[:answer4]))
  end

  def a(m)
    if m == "true"
      true
    else
      if m == "false"
        false
      else
        m
      end
    end
  end

#  def check2(choices, posted)

    
  def increment(touch_id)
    touch = Touch.find(touch_id)
    touch.score += 1
    touch.save
    touch.reload
    user = User.find(touch.user_id)
    user.score += 1
    user.save
  end

  def decrement(touch_id)
    touch = Touch.find(touch_id)
    touch.score -= 1
    touch.save
    touch.reload
    user = User.find(touch.user_id)
    user.score -= 1
    user.save
  end

  def retake
    @touch = Touch.where(params.require(:touch).permit(:user_id, :genre_id))[0]
    MultipleChoice.where(touch_id: @touch[:id]).destroy_all
    SingleChoice.where(touch_id: @touch[:id]).destroy_all
    @user = User.find(current_user[:id])
    @user.score -= @touch[:score]
    @user.save
    @genre = Genre.find(@touch.genre_id)
    @touch.destroy
    redirect_to "/" + @genre[:parent] + "/" + @genre[:subtype]
  end

end
