class CreateMultipleChoices < ActiveRecord::Migration[5.1]
  def change
    create_table :multiple_choices do |t|
      t.boolean :answer1
      t.boolean :answer2
      t.boolean :answer3
      t.boolean :answer4

      t.timestamps
    end
  end
end
