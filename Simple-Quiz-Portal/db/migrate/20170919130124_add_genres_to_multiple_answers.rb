class AddGenresToMultipleAnswers < ActiveRecord::Migration[5.1]
  def change
    add_reference :multiple_answers, :genre, foreign_key: true
  end
end
