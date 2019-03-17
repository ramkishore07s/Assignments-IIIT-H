class AddMultipleAnswersToMultipleChoices < ActiveRecord::Migration[5.1]
  def change
    add_reference :multiple_choices, :multiple_answer, foreign_key: true
  end
end
