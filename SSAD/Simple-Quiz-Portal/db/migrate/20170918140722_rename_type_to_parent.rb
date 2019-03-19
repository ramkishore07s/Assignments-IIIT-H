class RenameTypeToParent < ActiveRecord::Migration[5.1]
  def change
    rename_column :genres, :type, :parent
  end
end
