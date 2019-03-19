class AddScoreToTouches < ActiveRecord::Migration[5.1]
  def change
    add_column :touches, :score, :integer
  end
end
