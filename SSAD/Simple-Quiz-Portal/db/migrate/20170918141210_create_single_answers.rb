class CreateSingleAnswers < ActiveRecord::Migration[5.1]
  def change
    create_table :single_answers do |t|
      t.string :question
      t.string :option1
      t.string :option2
      t.string :option3
      t.string :option4
      t.string :answer

      t.timestamps
    end
  end
end
