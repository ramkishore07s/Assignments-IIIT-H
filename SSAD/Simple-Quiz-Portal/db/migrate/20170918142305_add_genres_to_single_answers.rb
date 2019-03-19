class AddGenresToSingleAnswers < ActiveRecord::Migration[5.1]
  def change
    add_reference :single_answers, :genre, foreign_key: true
  end
end
