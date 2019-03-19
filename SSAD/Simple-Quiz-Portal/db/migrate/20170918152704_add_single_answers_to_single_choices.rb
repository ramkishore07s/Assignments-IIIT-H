class AddSingleAnswersToSingleChoices < ActiveRecord::Migration[5.1]
  def change
    add_reference :single_choices, :single_answer, foreign_key: true
  end
end
